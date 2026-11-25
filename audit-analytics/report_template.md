# Audyt analityki i prywatności — $slug

- Data: $date
- Adres: `$url`
- **Wynik prywatności i zgód: $score/100** ($score_detail) — liczony skryptem z ruchu sieciowego; porównywalny między domenami, 100 = brak śledzenia bez zgody.
- Metoda: pasywna — trzy wczytania strony w świeżej przeglądarce (Chromium, pl-PL, 1440×900): A bez interakcji, B po „odrzuć”, C po „akceptuj”. Bez logowania, formularzy i skanowania.
- Tokeny z URL i dane osobowe są zamaskowane (`abcd…`).

## 1. Podsumowanie — 5 najważniejszych znalezisk

<!-- DO UZUPEŁNIENIA: tabela | # | Znalezisko | Waga (wysoka/średnia/niska) | Poprawka | Dowód (zrzut/sekcja) | -->

## Przebiegi

$passes

## 2. Zgody

$consent

<!-- DO UZUPEŁNIENIA: ocena — czy CMP blokuje tagi przed zgodą i po odrzuceniu (porównaj A/B/C); potwierdź albo skoryguj automatyczny tryb Consent Mode i jego kontrole na podstawie raw/. -->

## 3. Tagi

$tags

## 4. GA4 — żądania collect

$ga4

## 5. Wycieki danych do zewnętrznych hostów

Szukane: token z URL, e-maile, telefony — w URL żądania, nagłówku Referer i body.

$leaks

## 6. Odbiorcy danych

Hosty spoza domeny `$site_host`. Liczby = żądania w przebiegach A/B/C.

$recipients

## 7. Ciasteczka i storage

Narzędzie przypisane heurystycznie po nazwie ciasteczka.

$cookies

## 8. Polityka prywatności i administrator danych

$privacy

## 9. Wnioski: RODO i art. 399 Prawa komunikacji elektronicznej

<!-- DO UZUPEŁNIENIA: tylko fakty i potencjalne ryzyka, bez kwalifikacji prawnej. -->

## 10. E-commerce — zgodność z wytycznymi Google

Pushe `ecommerce` w dataLayer porównane z [referencją zdarzeń GA4](https://developers.google.com/analytics/devguides/collection/ga4/reference/events) i [wdrożeniem przez GTM](https://developers.google.com/analytics/devguides/collection/ga4/ecommerce?client_type=gtm). Audyt pasywny widzi tylko zdarzenia odpalane bez interakcji (np. `view_item_list`, `view_item`, `view_promotion`).

$ecommerce

## Dowody

Plansze generowane z przechwyconego ruchu (HAR): adres strony, czas wysłania, numer wpisu w `raw/<przebieg>/network.har`, parametry żądania z podświetlonymi danymi.

$evidence
