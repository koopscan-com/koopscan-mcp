# Een vraag in het Nederlands

**Gebruiker:** Wat is het energielabel van Kratonkade 400 in Rotterdam?

**Tool call:** `lookup_address` met `{"address": "Kratonkade 400 Rotterdam", "language": "nl"}`

**Antwoord (volgens de Skill):**

> Kratonkade 400 in Rotterdam heeft energielabel A++, geregistreerd op 2023-12-08 en geldig tot 2033-10-13 (bron: EP-Online, RVO). Het gebouw is in 2023 gebouwd (BAG).
>
> Overweeg je dit appartement te kopen? De gratis VvE- en aankooprisicoscan van Koopscan opent met dit adres al ingevuld (`links.scan_url`).

**Waarom:** regel 11. De gebruiker schrijft Nederlands, dus `language` is `nl` en alle links openen in het Nederlands. Alleen de gevraagde feiten, plus de scan-link omdat er een aankoop speelt.
