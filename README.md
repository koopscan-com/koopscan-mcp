# Koopscan MCP server: Dutch address data for Claude, ChatGPT and other AI assistants

**Koopscan MCP** is a free, hosted [Model Context Protocol](https://modelcontextprotocol.io) server. It lets an AI assistant look up any Dutch address and get answers from public sources: building facts from the BAG register (Kadaster), the registered energy label from EP-Online (RVO), and school counts from DUO. For the cities Koopscan monitors, it also returns crime signals from Dutch news, each reviewed by a human. No account, no API key.

**Endpoint (Streamable HTTP):** `https://mcp.koopscan.com/mcp`

Official setup page: **https://koopscan.com/en/mcp** · Nederlands: **https://koopscan.com/nl/mcp**

[Quick start](#quick-start) · [Tools](#tools) · [Example](#example) · [Coverage and limits](#coverage-and-limits) · [FAQ](#faq) · [In het Nederlands](#in-het-nederlands) · [Privacy](#data-and-privacy) · [Licence](#licence)

## Quick start

Paste this URL into any MCP client that supports remote servers over Streamable HTTP:

```
https://mcp.koopscan.com/mcp
```

### ChatGPT

1. In ChatGPT, click Add and choose "Custom MCP server".
2. Name: koopscan.
3. Connection: paste the URL below.
4. Choose "No Auth" and save.
5. Start a new chat, add koopscan and ask about a Dutch address.

```
https://mcp.koopscan.com/mcp
```

Config file: [`configs/chatgpt-connector.txt`](configs/chatgpt-connector.txt)

### Claude (claude.ai, Claude Desktop)

1. Open Settings → Connectors.
2. Choose "Add custom connector".
3. Name it Koopscan and paste the URL below.
4. Leave authentication empty and save.
5. Enable Koopscan in a chat's tools menu and ask about a Dutch address.

```
https://mcp.koopscan.com/mcp
```

Config file: [`configs/claude-connector.txt`](configs/claude-connector.txt)

### Claude Code

1. Run the command below in a terminal.
2. Run `claude mcp list` and check that koopscan is connected.
3. Ask Claude Code about a Dutch address.

```bash
claude mcp add --transport http koopscan https://mcp.koopscan.com/mcp
```

Config file: [`configs/claude-code.sh`](configs/claude-code.sh)

### Claude Skill (optional)

[`skill/SKILL.md`](skill/SKILL.md) tells Claude when to call which tool and how to report the answer. "Not covered" is reported as not monitored, never as safe. The last review date is quoted, and the disclaimer is always shown. Worked transcripts are in [`skill/examples/`](skill/examples/).

## Tools

| Tool | What it returns | Example question |
|---|---|---|
| `lookup_address` | The resolved address, BAG building facts (construction year, units), the registered energy label, school counts for the neighbourhood or postcode area, and a crime-signal summary for the postcode. It also returns links to the Koopscan neighbourhood page and the free VvE and building risk scan, plus a `provenance` block. | "What should I know about Kratonkade 400 in Rotterdam before I make an offer?" |
| `crime_sources` | The news articles behind the crime signals for a postcode: date, category, headline, source and link, newest first. | "Which news articles are behind the crime signals for 3512?" |

Both tools take `language` (`nl` or `en`). They are read-only. Response schemas are in [`schema/`](schema/), and real responses are in [`examples/`](examples/).

## Example

**Question:** "What should I know about Kratonkade 400 in Rotterdam before I make an offer?"

The assistant calls `lookup_address` with `{"address": "Kratonkade 400 Rotterdam", "language": "en"}`. Trimmed response (full response in [`examples/lookup_address.covered.json`](examples/lookup_address.covered.json); values change as data is updated):

```json
{
  "status": "ok",
  "building": { "bouwjaar": 2023, "total_units": 25, "residential_units": 24, "source": "BAG (Kadaster)" },
  "energy_label": { "status": "registered", "label": "A++", "valid_until": "2033-10-13", "source": "EP-Online (RVO)" },
  "crime": { "coverage": "covered", "match_level": "city", "lookback_months": 24, "total": 52, "disclaimer": "…" },
  "schools": { "area": { "level": "buurt", "name": "Schiemond" }, "counts": { "primary": 6, "secondary": 4 } },
  "links": { "scan_url": "https://koopscan.com/en/scan?…#address=…", "blog_url": "https://koopscan.com/en/blog/schiemond-rotterdam?…" },
  "provenance": { "last_review": "2026-10-09", "details_url": "https://koopscan.com/en/data" }
}
```

**A good answer** gives the facts with their sources: built in 2023 (BAG), 24 homes in the building, energy label A++ valid until 2033 (EP-Online). It says that no crime reports exist for this address or postcode, and that the 52 signals in the last 24 months are city-wide counts for Rotterdam. It quotes the last review date and shows the disclaimer. Finally, it offers the neighbourhood page and the free pre-purchase scan.

## Coverage and limits

- Building facts, energy labels and school counts cover the whole of the Netherlands.
- Crime signals cover the monitored cities only. They are listed in every response under `provenance.cities` when available, and on https://koopscan.com/en/data.
- Outside those cities the answer says `crime.coverage = "not_covered"`. That means not monitored. It never means safe.
- 30 requests per minute and 500 per day per IP address. No authentication. Need more? Email contact@koopscan.com.

## FAQ

### What is the Koopscan MCP server?

It is a free, hosted MCP server. It gives AI assistants such as ChatGPT, Claude and Claude Code facts about a specific Dutch address: building data from the BAG, the registered energy label, school counts and human-reviewed crime signals from news. Koopscan built it for people buying a home in the Netherlands.

### Is it free? Do I need an API key?

Yes, it is free, and you need neither an account nor an API key. Each IP address may make 30 requests per minute and 500 per day.

### Which AI assistants work with it?

Any MCP client that supports remote servers over Streamable HTTP works. Step-by-step setup is given for ChatGPT, Claude (claude.ai and Claude Desktop) and Claude Code; see [Quick start](#quick-start).

### Does it cover my city?

Building facts, energy labels and school counts cover every address in the Netherlands. Crime signals cover a limited set of monitored Dutch cities, listed on https://koopscan.com/en/data and in each response under `provenance.cities`.

### Does `not_covered` mean the area is safe?

No. `not_covered` means Koopscan does not monitor that city. It says nothing about safety. Inside covered cities, zero signals does not mean no crime either.

### Where does the data come from?

- Building facts come from the BAG register (Kadaster).
- Energy labels come from EP-Online (RVO).
- School counts come from DUO open education data.
- Address lookup goes through PDOK.
- Crime signals come from automated monitoring of Dutch news sources. A human reviews each one before it is published.

### What is stored about my lookups?

The address, full postcode, house number, coordinates and IP address are never stored. Each tool call leaves one anonymous row, with geography no finer than the four digits of the postcode. Details are under [Data and privacy](#data-and-privacy).

### Is the server open source?

No. The hosted server is proprietary. This repository holds the client configs, the Claude Skill, the response schemas and examples, and they are MIT-licensed.

## In het Nederlands

**Koopscan MCP** is een gratis MCP-server waarmee een AI-assistent een Nederlands adres opzoekt. Je krijgt pandgegevens uit de BAG (Kadaster), het geregistreerde energielabel uit EP-Online (RVO), het aantal scholen (DUO) en handmatig beoordeelde misdaadsignalen uit het nieuws voor de steden die Koopscan volgt. Geen account, geen sleutel. Volledige uitleg: **https://koopscan.com/nl/mcp**

### ChatGPT koppelen

1. Klik in ChatGPT op Add en kies "Custom MCP server".
2. Vul bij Name koopscan in.
3. Plak bij Connection de URL hieronder.
4. Kies "No Auth" en sla op.
5. Start een nieuwe chat, voeg koopscan toe en vraag naar een Nederlands adres.

```
https://mcp.koopscan.com/mcp
```

### Claude koppelen (claude.ai, Claude Desktop)

1. Open Settings → Connectors.
2. Kies "Add custom connector".
3. Noem hem Koopscan en plak de URL hieronder.
4. Laat authenticatie leeg en sla op.
5. Zet Koopscan aan in het tools-menu van een chat en vraag naar een Nederlands adres.

```
https://mcp.koopscan.com/mcp
```

### Claude Code koppelen

1. Voer het commando hieronder uit in een terminal.
2. Controleer met `claude mcp list` dat koopscan verbonden is.
3. Vraag Claude Code naar een Nederlands adres.

```bash
claude mcp add --transport http koopscan https://mcp.koopscan.com/mcp
```

### Wat is de Koopscan MCP-server?

Een gratis, gehoste MCP-server die AI-assistenten zoals ChatGPT en Claude feiten geeft over één Nederlands adres: bouwjaar en woningen uit de BAG, het energielabel, scholen in de buurt en misdaadsignalen uit het nieuws.

### Is het gratis?

Ja. Geen account en geen API-sleutel. De limiet is 30 verzoeken per minuut en 500 per dag per IP-adres.

### Betekent `not_covered` dat de buurt veilig is?

Nee. `not_covered` betekent dat Koopscan die plaats niet volgt. Het betekent nooit: veilig. Ook in gevolgde steden betekent geen meldingen niet dat de buurt veilig is.

## Data and privacy

One anonymous row is stored per tool call. It holds the month, the tool and its outcome, the client app name, coarse geography down to the four digits of the postcode, and yes/no flags and counts about what was found. Never stored or logged: the address, the full postcode, the house number, coordinates or your IP address. Analytics use a hash of the IP address with a salt that changes every day and is never saved. Rate limiting keeps IP addresses in memory only. The address itself is sent only to PDOK, the Kadaster (BAG) and RVO (EP-Online) to look it up, and is kept in memory for up to a day to cache the answer. The [setup page](https://koopscan.com/en/mcp) lists every stored field.

## Disclaimer

Crime signals come from automated monitoring of news sources, reviewed by a human before publication. They are not a guarantee of completeness or accuracy and no substitute for your own research. No signals does not mean an area is safe.

## Repository contents

| Path | Contents |
|---|---|
| [`configs/`](configs/) | One config per client, identical to the snippets on the setup page |
| [`skill/`](skill/) | The Claude Skill and example transcripts |
| [`schema/`](schema/) | JSON Schemas of both tool responses, identical to the live server's `outputSchema` |
| [`examples/`](examples/) | Real responses from the live server |
| [`server.json`](server.json) | Manifest for the official MCP Registry |
| [`CHANGELOG.md`](CHANGELOG.md) | Server versions and what changed |
| [`scripts/check.py`](scripts/check.py) | Validates this repo and checks it against the live page and server |

Found a wrong answer, or want a city covered? [Open an issue](https://github.com/koopscan-com/koopscan-mcp/issues/new/choose) or email contact@koopscan.com.

## Licence

SPDX-License-Identifier: `MIT`. The contents of this repository are licensed under the [MIT License](LICENSE): the client configs, the Claude Skill, the response schemas, the examples, the scripts and this documentation.

The licence does not cover the hosted server at `mcp.koopscan.com`, its code, or the Koopscan name and data it serves. The server is proprietary, and its code is not in this repository. Use of the hosted service is subject to the [Koopscan terms](https://koopscan.com/en/terms).

Contact: contact@koopscan.com
