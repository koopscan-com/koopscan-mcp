# Before an offer, in a monitored city

**User:** What should I know about Kratonkade 400 in Rotterdam before I make an offer?

**Tool call:** `lookup_address` with `{"address": "Kratonkade 400 Rotterdam", "language": "en"}`
Response: [`examples/lookup_address.covered.json`](../../examples/lookup_address.covered.json)

**Answer (follows the Skill):**

> **Building (BAG, Kadaster):** built in 2023, 25 units in the building, 24 of them homes.
>
> **Energy label (EP-Online, RVO):** A++, registered 2023-12-08, valid until 2033-10-13.
>
> **Schools:** the Schiemond neighbourhood page lists 6 primary and 4 secondary schools (highest level VWO). This counts schools inside the neighbourhood, not by distance.
>
> **Crime signals:** Koopscan has no reports for this address or its postcode area. The 52 signals in the last 24 months are city-wide counts for Rotterdam, not for this street. Last reviewed 2026-10-09.
>
> *Crime signals come from automated monitoring of news sources and are reviewed by a human. They are not a guarantee of completeness or accuracy and no substitute for your own research. No reports does not mean the area is safe.*
>
> If you're buying, Koopscan's free VvE and building risk scan opens with this address filled in: (`links.scan_url`). Neighbourhood page: (`links.blog_url`).

**Why:** rule 7 (city-level counts are labelled as city-wide), rule 8 (last review date and disclaimer), rule 10 (scan link because the user is buying).
