# Changelog

Versions of the hosted Koopscan MCP server at `https://mcp.koopscan.com/mcp`. A `!` marks a change to the response shape. The schemas in [`schema/`](schema/) always match the newest version. Data updates (reviewed signals, new cities) are logged on https://koopscan.com/en/data.

## 0.7.0 (2026-10-09)

- `provenance.cities` lists every city with signals. City-wide crime categories are returned when there are no reports for the address or its postcode area (`crime.match_level = "city"`). (!)
- `details_url` links point to sections (anchors) of the Koopscan neighbourhood page.

## 0.6.0 (2026-10-08)

- `links.vve_report_url` is removed. `links.scan_url` is the one link to the free VvE and building risk report. (!)

## 0.5.1 (2026-10-08)

- The tool description now steers clients to `links.scan_url` when the user asks for a report.

## 0.5.0 (2026-10-06)

- New `links.scan_url`: opens the scan page with the address filled in. The address is carried only in the URL fragment. (!)

## 0.4.0 (2026-10-06)

- New `lookup_address.schools`: primary and secondary school counts for the neighbourhood page or the 4-digit postcode area. (!)

## 0.3.0 (2026-10-05)

- New `links.setup_url` on successful lookups. (!)

## 0.2.1 (2026-10-05)

- Tool input schemas no longer gain extra required arguments from instrumentation.

## 0.2.0 (2026-09-26)

- New `provenance` block (signals reviewed, confirmed and rejected; last review date). The disclaimer is dated and built from published counters. (!)

## 0.1.0 (2026-09-15)

- First release: `lookup_address` and `crime_sources`.
