# Audyt analityki i prywatności — comperiaraty

- Data: 2026-11-25
- Adres: `https://comperiaraty.pl/`
- Metoda: pasywna — trzy wczytania strony w świeżej przeglądarce (Chromium, pl-PL, 1440×900): A bez interakcji, B po „odrzuć”, C po „akceptuj”. Bez logowania, formularzy i skanowania.
- Tokeny z URL i dane osobowe są zamaskowane (`abcd…`).

## 1. Podsumowanie — 5 najważniejszych znalezisk

Strona wysyła mało danych na zewnątrz — są tylko 4 znaleziska, piątego nie dopisano bez dowodu.

| # | Znalezisko | Waga | Poprawka | Dowód |
|---|---|---|---|---|
| 1 | Brak jakiegokolwiek pomiaru (GA4, GTM, piksele) na stronie z wnioskiem pożyczkowym — lejek „Złóż wniosek” jest niemierzony, przynajmniej po stronie przeglądarki. | średnia | Jeśli pomiar jest potrzebny: GTM + GA4 z CMP i `consent default` = denied od pierwszego wdrożenia. | 00, sekcja 3 |
| 2 | Kalkulator pobiera ofertę przez JSONP z innej domeny (`www.comperia.pl/ajax/calculateBestOffer.php?...&callback=jQuery…`) — kwota i okres trafiają do comperia.pl. | niska | Zastąp JSONP żądaniem `fetch` z nagłówkami CORS albo endpointem na własnej domenie. | sekcja 6 |
| 3 | Fonty ładowane z `fonts.googleapis.com` / `fonts.gstatic.com` (9 żądań) — adres IP odwiedzającego trafia do Google. | niska | Hostuj fonty lokalnie. | sekcja 6 |
| 4 | Strona główna nie wskazuje administratora danych; wskazuje go polityka prywatności (`/polityka-prywatnosci/`). | niska | Dodaj nazwę administratora w stopce albo przy formularzu wniosku. | sekcja 8 |

## Przebiegi

| Przebieg | Kliknięto | Przycisk „odrzuć” | Przycisk „akceptuj” | Żądania |
|---|---|---|---|---|
| A | — | — | — | 87 |

Pominięte przebiegi: B, C — brak odpowiedniego przycisku w banerze (przebieg A).

## 2. Zgody

- CMP: nie wykryto; IAB TCF (`__tcfapi`): nie.

**Tryb Consent Mode (automatycznie): nie dotyczy — brak żądań GA4**

_brak_

**Komendy `gtag('consent', …)` w dataLayer**

_brak_

**Parametry Consent Mode w żądaniach GA4** (faza = przed/po kliknięciu w baner)

_brak_

**Żądania narzędzi śledzących/monitorujących**

_brak_

**Ocena:** Strona nie ma banera zgód, dlatego przebiegi B i C pominięto. W `raw/A/` brak dataLayer (`null`), brak ciasteczek i brak żądań do narzędzi śledzących — przy obecnym stanie baner nie jest potrzebny do żadnego tagu. Skrypt `sce.comperiaraty.pl` widoczny na comperia.pl nie ładuje się na tej domenie.

## 3. Tagi

_brak_

- Wczytania skryptów GTM/gtag w przebiegu A: brak.
- `page_view` na identyfikator GA4 w przebiegu A: brak.
- Server-side GTM / własny endpoint: nie wykryto.

- Globalne obiekty (A): .
- Narzędzia wg żądań (wszystkie przebiegi): Google Fonts ×9.

## 4. GA4 — żądania collect

Zdarzenia: brak

_brak_

## 5. Wycieki danych do zewnętrznych hostów

Szukane: token z URL, e-maile, telefony — w URL żądania, nagłówku Referer i body.

_brak_

## 6. Odbiorcy danych

Hosty spoza domeny `comperiaraty.pl`. Liczby = żądania w przebiegach A/B/C.

| Host | Firma / narzędzie | A | B | C | Jakie dane |
|---|---|---|---|---|---|
| fonts.gstatic.com | Google / Google Fonts | 8 | — | — | zasoby statyczne |
| fonts.googleapis.com | Google / Google Fonts | 1 | — | — | Referer ze stroną |
| www.comperia.pl | Comperia / kalkulator (JSONP) | 1 | — | — | Referer ze stroną |

## 7. Ciasteczka i storage

Narzędzie przypisane heurystycznie po nazwie ciasteczka.

_brak_

Klucze localStorage: brak.  
Klucze sessionStorage: wpEmojiSettingsSupports.

## 8. Polityka prywatności i administrator danych

- Linki o prywatności/cookies na stronie: 1.
- Strona wprost wskazuje administratora danych: nie znaleziono.

| Tekst linku | URL | HTTP | Wzmianka o administratorze |
|---|---|---|---|
| Polityka prywatności | https://comperiaraty.pl/polityka-prywatnosci/ | 200 | True |

## 9. Wnioski: RODO i art. 399 Prawa komunikacji elektronicznej

- Fakt: strona nie zapisuje ciasteczek ani localStorage; w sessionStorage jest tylko `wpEmojiSettingsSupports` (WordPress, wykrywanie emoji). Ryzyko w zakresie art. 399 PKE: nie wykryto.
- Fakt: fonty Google i wywołanie kalkulatora na `www.comperia.pl` przekazują adres IP i Referer stronom trzecim (comperia.pl to powiązana marka). Ryzyko: przekazanie IP do Google bez informacji w banerze może wymagać opisu w polityce prywatności.
- Audyt objął tylko stronę główną bez wypełniania wniosku — przetwarzanie danych z formularza nie było badane.

## 10. E-commerce — zgodność z wytycznymi Google

Pushe `ecommerce` w dataLayer porównane z [referencją zdarzeń GA4](https://developers.google.com/analytics/devguides/collection/ga4/reference/events) i [wdrożeniem przez GTM](https://developers.google.com/analytics/devguides/collection/ga4/ecommerce?client_type=gtm). Audyt pasywny widzi tylko zdarzenia odpalane bez interakcji (np. `view_item_list`, `view_item`, `view_promotion`).

Przebieg A, strony: `https://comperiaraty.pl/`.

Nie dotyczy — strona nie prowadzi sprzedaży.

## Dowody

Plansze generowane z przechwyconego ruchu (HAR): adres strony, czas wysłania, numer wpisu w `raw/<przebieg>/network.har`, parametry żądania z podświetlonymi danymi.

- `screenshots/00-strona.png` — strona i adres (przebieg A)
