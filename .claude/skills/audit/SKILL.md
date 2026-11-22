---
name: audit
description: Audyt SEO i dostępności domeny — deterministyczny raport z kodu (strona startowa + do 10 stron z sitemapy, Lighthouse 0–100, axe-core) i krytyczna ocena niezależnego audytora w osobnym pliku. Użyj, gdy użytkownik wpisze /audit <url>.
argument-hint: <url>
disable-model-invocation: true
context: fork
agent: auditor
---

Przeprowadź niezależny audyt domeny: $ARGUMENTS

Audytujesz tylko tę domenę. Nie korzystaj z wiedzy o innych audytach ani raportach w `audit-seo/reports/` — oceniasz wyłącznie raport wygenerowany w tym uruchomieniu.
