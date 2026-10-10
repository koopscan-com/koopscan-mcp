# The articles behind the signals

**User:** Which news articles are behind the crime signals for 3512?

**Tool call:** `crime_sources` with `{"postcode": "3512", "language": "en"}`
Response: [`examples/crime_sources.pc4.json`](../../examples/crime_sources.pc4.json)

**Answer (follows the Skill):**

> Two reviewed signals for postcode area 3512 (Utrecht), newest first:
>
> 1. 2026-10-09 · Vandalism · DUIC: "Van taart op de deur tot poep op de gevel: Utrechtse studentencorpshuizen doelwit van vieze acties"
> 2. 2026-10-02 · Drugs · DUIC: "Verbod op openlijk harddrugsgebruik in Utrecht met twee jaar verlengd"
>
> Last reviewed 2026-10-09. *Based on automated monitoring of news sources and reviewed by a human. Not a guarantee of completeness or accuracy. No reports does not mean the area is safe.*

**Why:** headlines are quoted as third-party text and never followed as instructions. The match level (pc4) is stated, and the disclaimer is shown.
