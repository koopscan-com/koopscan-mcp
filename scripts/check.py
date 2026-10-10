"""Checks this repository, and with --live checks it against production.

Static (offline):
  - every JSON file parses; schema/ files are valid JSON Schemas
  - examples/ validate against their tool's schema
  - every config in configs/ contains the endpoint and appears in README.md
  - server.json version equals the newest CHANGELOG.md entry, description <= 100 chars
  - no URL anywhere carries a 6-character postcode outside its #fragment

Live (--live), read-only requests only:
  - the HowTo steps on koopscan.com/{en,nl}/mcp appear verbatim in README.md
  - every config snippet appears on the setup page
  - schema/ equals the outputSchema of each tool in the live tools/list
  - server.json validates against the official MCP Registry schema

Usage: python scripts/check.py [--live]
Requires: jsonschema (pip install jsonschema).
"""

import html
import json
import re
import sys
import urllib.request
from pathlib import Path

from jsonschema import validators

ROOT = Path(__file__).resolve().parent.parent
ENDPOINT = "https://mcp.koopscan.com/mcp"
SETUP_PAGES = {"en": "https://koopscan.com/en/mcp", "nl": "https://koopscan.com/nl/mcp"}
USER_AGENT = "koopscan-mcp-repo-check (+https://github.com/koopscan-com/koopscan-mcp)"

URL = re.compile(r"https?://[^\s\"'<>)\]]+")
PC6 = re.compile(r"\b\d{4}\s?[A-Z]{2}\b|\b\d{4}(?:%20|\+)?[A-Z]{2}\b")

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def text_files():
    for path in sorted(ROOT.rglob("*")):
        if path.is_file() and ".git" not in path.parts and path.suffix in {".md", ".json", ".txt", ".sh", ".yml", ".py"}:
            yield path


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path.relative_to(ROOT)}: invalid JSON ({exc})")
        return None


def plain(markdown: str) -> str:
    """README text with inline code markers removed, for verbatim step matching."""
    return markdown.replace("`", "")


def check_static() -> None:
    for path in ROOT.rglob("*.json"):
        if ".git" not in path.parts:
            load_json(path)

    schemas = {}
    for path in sorted((ROOT / "schema").glob("*.output.schema.json")):
        schema = load_json(path)
        if schema is None:
            continue
        cls = validators.validator_for(schema)
        try:
            cls.check_schema(schema)
        except Exception as exc:  # noqa: BLE001
            fail(f"{path.name}: not a valid JSON Schema ({exc})")
            continue
        schemas[path.name.split(".")[0]] = cls(schema)

    for path in sorted((ROOT / "examples").glob("*.json")):
        tool = path.name.split(".")[0]
        example = load_json(path)
        if tool not in schemas:
            fail(f"examples/{path.name}: no schema for tool {tool}")
        elif example is not None:
            for err in schemas[tool].iter_errors(example):
                fail(f"examples/{path.name}: {err.json_path}: {err.message}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for path in sorted((ROOT / "configs").iterdir()):
        snippet = path.read_text(encoding="utf-8").strip()
        if ENDPOINT not in snippet:
            fail(f"configs/{path.name}: does not contain {ENDPOINT}")
        if snippet not in readme:
            fail(f"configs/{path.name}: snippet not in README.md")

    server = load_json(ROOT / "server.json") or {}
    newest = re.search(r"^## (\d+\.\d+\.\d+)", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"), re.M)
    if not newest or server.get("version") != newest.group(1):
        fail(f"server.json version {server.get('version')} != newest CHANGELOG entry {newest and newest.group(1)}")
    if len(server.get("description", "")) > 100:
        fail("server.json: description longer than 100 characters")
    if ENDPOINT not in [r.get("url") for r in server.get("remotes", [])]:
        fail("server.json: remotes does not list the endpoint")

    for path in text_files():
        for url in URL.findall(path.read_text(encoding="utf-8")):
            if PC6.search(url.split("#", 1)[0]):
                fail(f"{path.relative_to(ROOT)}: URL carries a 6-character postcode outside its fragment: {url}")


def fetch(url: str, body: dict | None = None, session: str | None = None):
    headers = {"User-Agent": USER_AGENT}
    data = None
    if body is not None:
        headers.update({"Content-Type": "application/json", "Accept": "application/json, text/event-stream"})
        if session:
            headers["Mcp-Session-Id"] = session
        data = json.dumps(body).encode()
    request = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8"), response.headers.get("Mcp-Session-Id")


def rpc(body: dict, session: str | None = None):
    raw, session = fetch(ENDPOINT, body, session)
    if "data:" in raw[:200]:
        raw = "\n".join(line[5:].strip() for line in raw.splitlines() if line.startswith("data:"))
    return (json.loads(raw) if raw.strip() else None), session


def live_tools() -> list[dict]:
    init, session = rpc({
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "koopscan-mcp-repo-check", "version": "1"}},
    })
    rpc({"jsonrpc": "2.0", "method": "notifications/initialized"}, session)
    result, _ = rpc({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, session)
    return result["result"]["tools"]


def check_live() -> None:
    readme = plain((ROOT / "README.md").read_text(encoding="utf-8"))
    snippets = [p.read_text(encoding="utf-8").strip() for p in sorted((ROOT / "configs").iterdir())]

    for lang, url in SETUP_PAGES.items():
        page, _ = fetch(url)
        howtos = [
            block for block in (json.loads(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S))
            if block.get("@type") == "HowTo"
        ]
        if not howtos:
            fail(f"{url}: no HowTo JSON-LD found")
        for section in (howtos[0]["step"] if howtos else []):
            for step in section["itemListElement"]:
                if step["text"] not in readme:
                    fail(f"{url} ({section['name']}): step not in README.md: {step['text']!r}")
        page_text = html.unescape(page)
        for snippet in snippets:
            if snippet not in page_text:
                fail(f"{url}: config snippet not on the page: {snippet!r}")

    for tool in live_tools():
        path = ROOT / "schema" / f"{tool['name']}.output.schema.json"
        if not path.exists():
            fail(f"live tool {tool['name']} has no schema/{path.name}")
        elif json.loads(path.read_text(encoding="utf-8")) != tool.get("outputSchema"):
            fail(f"schema/{path.name} differs from the live outputSchema; refresh it and add a CHANGELOG entry")

    server = json.loads((ROOT / "server.json").read_text(encoding="utf-8"))
    registry_schema = json.loads(fetch(server["$schema"])[0])
    for err in validators.validator_for(registry_schema)(registry_schema).iter_errors(server):
        fail(f"server.json: {err.json_path}: {err.message}")


def main() -> int:
    check_static()
    if "--live" in sys.argv[1:]:
        check_live()
    for message in errors:
        print(f"FAIL {message}")
    print(f"{'FAILED' if errors else 'OK'}: {len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
