# A city Koopscan does not monitor

**User:** Is Grote Markt 1 in Groningen in a safe area?

**Tool call:** `lookup_address` with `{"address": "9712HN 1", "language": "en"}`
Response: [`examples/lookup_address.not_covered.json`](../../examples/lookup_address.not_covered.json)

**Answer (follows the Skill):**

> Koopscan does not monitor crime signals in Groningen (`crime.coverage` is `not_covered`), so I can't tell you anything about safety from this source. That is not the same as the area being safe. The municipality's or the police's own figures are a better source for this.
>
> What I can tell you: the building dates from 1813 (BAG) and has energy label A+++, valid until 2033-07-11 (EP-Online).

**Why:** rule 5. "Not covered" is reported as not monitored and never as safe. Zero signals are not read as "no crime".
