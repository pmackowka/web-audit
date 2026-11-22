# Audyt analityki i prywatności — gemini-staffly

- Data: 2026-11-20
- Adres: `https://gemini.staffly.pl/psychometry-test/7ea9…`
- Metoda: pasywna — trzy wczytania strony w świeżej przeglądarce (Chromium, pl-PL, 1440×900): A bez interakcji, B po „odrzuć”, C po „akceptuj”. Bez logowania, formularzy i skanowania.
- Tokeny z URL i dane osobowe są zamaskowane (`abcd…`).

## 1. Podsumowanie — 5 najważniejszych znalezisk

> Zakres: link testu był już nieaktywny — audyt obejmuje widok „Ten link nie jest już aktywny” (`screenshots/00-strona.png`). Baneru zgód brak, więc przebiegi B i C pominięto. Na stronie są przyciski ankiety i „Prześlij odpowiedź” — nie klikano ich.

| # | Znalezisko | Waga | Poprawka | Dowód |
|---|---|---|---|---|
| 1 | Token testu z URL (`/psychometry-test/7ea9…`) trafia do GA4 w `dl` (`page_view`, `scroll`) i `dr` (drugi `page_view`) | wysoka | Przed wysyłką zastąpić token w `page_location`/`page_referrer` stałą ścieżką (np. `/psychometry-test/:token`) — w konfiguracji tagu GA4 albo w sGTM | `screenshots/E02-A-google-analytics-4.png`, sekcje 4, 5 |
| 2 | Datadog RUM dostaje token w `view.url`/`referrer`, a JWT `testAccessToken` (ważny 365 dni: iat 2026-11-04, exp 2027-11-05) w `view.url` po przejściu SPA na `/psychometry-test/<JWT>/pl`, w `referrer` i w URL zasobu `api-hr.staffly.pl/.../test/<JWT>` | wysoka | `beforeSend` w Datadog RUM maskujący tokeny w `view.url`, `view.referrer`, `resource.url`; JWT poza URL (nagłówek `Authorization`); krótsza ważność | `screenshots/E01-A-datadog-rum-logs.png`, sekcje 5, 6 |
| 3 | Brak CMP i jakiejkolwiek zgody: GA4, Datadog RUM i Session Replay startują w 0,4 s od wejścia, ustawiają `_ga`, `_ga_06GR0KC78D` (400 dni) i `_dd_s` | wysoka | Wdrożyć CMP; GA4 i Session Replay uruchamiać po zgodzie; Consent Mode v2 z `default` denied | `screenshots/00-strona.png`, `E02`, `E03`, sekcje 2, 7 |
| 4 | Datadog Session Replay nagrywa sesję na stronie testu psychometrycznego (`session_replay_sample_rate: 20`, w tym przebiegu 8 wysyłek `/api/v2/replay`) | średnia | Wyłączyć replay na ścieżkach testu albo `defaultPrivacyLevel: 'mask'`; replay tylko po zgodzie | `screenshots/E03-A-datadog-session-replay.png`, sekcje 2, 3 |
| 5 | Widok nie zawiera linku do polityki prywatności ani informacji o administratorze danych | średnia | Stopka z linkiem do polityki prywatności i polityki cookies na każdym widoku testu | `screenshots/00-strona.png`, sekcja 8 |

## Przebiegi

| Przebieg | Kliknięto | Przycisk „odrzuć” | Przycisk „akceptuj” | Żądania |
|---|---|---|---|---|
| A | — | — | — | 73 |

Pominięte przebiegi: B, C — brak odpowiedniego przycisku w banerze (przebieg A).

## 2. Zgody

- CMP: nie wykryto; IAB TCF (`__tcfapi`): nie.

**Komendy `gtag('consent', …)` w dataLayer**

_brak_

**Parametry Consent Mode w żądaniach GA4** (faza = przed/po kliknięciu w baner)

| Przebieg | Faza | gcs | gcd | Zdarzenia GA4 |
|---|---|---|---|---|
| A | przed | — | 13l3l3l2l1l1 | 3 |

**Żądania narzędzi śledzących/monitorujących**

| Przebieg | Faza | Narzędzie × żądania |
|---|---|---|
| A | przed | Datadog Session Replay ×8; Datadog RUM / Logs ×5; Google Analytics 4 ×2; Google tag (gtag.js) ×1 |

**Ocena:** nie ma mechanizmu zgód. Wszystkie żądania GA4 i Datadog wysłano bez interakcji (faza „przed”). W dataLayer brak komend `gtag('consent', …)`, a żądania GA4 nie mają parametru `gcs` — Consent Mode nie jest skonfigurowany. Obecny `gcd=13l3l3l2l1l1` (raport surowy, liter nie interpretujemy) i `npa=1`. Porównanie z B/C niemożliwe — brak baneru.

## 3. Tagi

| Typ | Identyfikatory |
|---|---|
| GA4 | G-06GR0KC78D |

- Wczytania skryptów GTM/gtag w przebiegu A: G-06GR0KC78D ×1.
- `page_view` na identyfikator GA4 w przebiegu A: G-06GR0KC78D ×2.
- Server-side GTM / własny endpoint: nie wykryto.
- Datadog Session Replay: body żądań `/api/v2/replay` to blob multipart — Playwright go nie zapisuje; ocena tylko na podstawie faktu wysyłki.
- Globalne obiekty (A): datadog_rum.
- Narzędzia wg żądań (wszystkie przebiegi): Datadog Session Replay ×8; Datadog RUM / Logs ×5; Google Fonts ×3; Google Analytics 4 ×2; Google tag (gtag.js) ×1.

## 4. GA4 — żądania collect

Zdarzenia: A: page_view ×2, A: scroll ×1

| Przebieg | Faza | t [s] | en | tid | cid | sid | dl | dr | gcs | gcd | ep./up. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | przed | 0.417 | page_view | G-06GR0KC78D | 1882853944.1795176250 | 1795176250 | https://gemini.staffly.pl/psychometry-test/7ea9… | — | — | 13l3l3l2l1l1 | — |
| A | przed | 5.428 | scroll | G-06GR0KC78D | 1882853944.1795176250 | 1795176250 | https://gemini.staffly.pl/psychometry-test/7ea9… | — | — | 13l3l3l2l1l1 | {"epn.percent_scrolled": "90"} |
| A | przed | 5.428 | page_view | G-06GR0KC78D | 1882853944.1795176250 | 1795176250 | https://gemini.staffly.pl/psychometry-test/inactive/pl | https://gemini.staffly.pl/psychometry-test/7ea9… | — | 13l3l3l2l1l1 | — |

## 5. Wycieki danych do zewnętrznych hostów

Szukane: token z URL, e-maile, telefony — w URL żądania, nagłówku Referer i body.

| Przebieg | Faza | t [s] | Host | Gdzie | Co | Dowód |
|---|---|---|---|---|---|---|
| A | przed | 0.417 | region1.google-analytics.com | URL | token 7ea9… (pola: dl) | `screenshots/E02-A-google-analytics-4.png` |
| A | przed | 0.474 | browser-intake-datadoghq.eu | body | token 7ea9… (pola: url) | `screenshots/E01-A-datadog-rum-logs.png` |
| A | przed | 0.48 | browser-intake-datadoghq.eu | body | token 7ea9… (pola: referrer, url) | `screenshots/E01-A-datadog-rum-logs.png` |
| A | przed | 0.48 | browser-intake-datadoghq.eu | body | token 7ea9… (pola: url) | `screenshots/E01-A-datadog-rum-logs.png` |
| A | przed | 0.501 | browser-intake-datadoghq.eu | body | token 7ea9… (pola: dl, referrer, url) | `screenshots/E01-A-datadog-rum-logs.png` |
| A | przed | 1.068 | browser-intake-datadoghq.eu | body | token 7ea9… (pola: referrer, url); JWT (pola: referrer, url) | `screenshots/E01-A-datadog-rum-logs.png` |
| A | przed | 5.428 | region1.google-analytics.com | URL | token 7ea9… (pola: dl) | `screenshots/E02-A-google-analytics-4.png` |
| A | przed | 5.428 | region1.google-analytics.com | body | token 7ea9… (pola: dr) | `screenshots/E02-A-google-analytics-4.png` |

## 6. Odbiorcy danych

Hosty spoza domeny `gemini.staffly.pl`. Liczby = żądania w przebiegach A/B/C.

| Host | Firma / narzędzie | A | B | C | Jakie dane |
|---|---|---|---|---|---|
| browser-intake-datadoghq.eu | Datadog / Datadog RUM / Logs | 13 | — | — | Referer ze stroną, URL strony w parametrach/body, ⚠ JWT, ⚠ token |
| fonts.gstatic.com | Google / Google Fonts | 3 | — | — | Referer ze stroną |
| region1.google-analytics.com | Google / Google Analytics | 2 | — | — | Referer ze stroną, URL strony w parametrach/body, cid/sid (identyfikatory GA), ⚠ token |
| www.googletagmanager.com | Google / Google tag (gtag.js) | 1 | — | — | Referer ze stroną |

## 7. Ciasteczka i storage

Narzędzie przypisane heurystycznie po nazwie ciasteczka.

| Nazwa | Domena | Ważność | Narzędzie | A | B | C |
|---|---|---|---|---|---|---|
| _dd_s | gemini.staffly.pl | 365 dni | Datadog RUM | ✔ | n/d | n/d |
| _ga | .staffly.pl | 400 dni | Google Analytics 4 | ✔ | n/d | n/d |
| _ga_06GR0KC78D | .staffly.pl | 400 dni | Google Analytics 4 | ✔ | n/d | n/d |
| connect.sid | api-hr.staffly.pl | sesja | ? | ✔ | n/d | n/d |

Klucze localStorage: brak.  
Klucze sessionStorage: brak.

## 8. Polityka prywatności i administrator danych

- Linki o prywatności/cookies na stronie: 0.
- Strona wprost wskazuje administratora danych: nie znaleziono.

_brak_

## 9. Wnioski: RODO i art. 399 Prawa komunikacji elektronicznej

Fakty i potencjalne ryzyka, bez kwalifikacji prawnej:

- **Art. 399 PKE:** przed jakąkolwiek interakcją w urządzeniu użytkownika zapisano `_ga`, `_ga_06GR0KC78D` (analityka, 400 dni) i `_dd_s` (Datadog). Ciasteczka analityczne zwykle nie są traktowane jako niezbędne do świadczenia usługi — ich zapis bez zgody może stanowić ryzyko.
- **RODO — minimalizacja i integralność:** token testu i JWT identyfikują konkretnego kandydata w procesie rekrutacyjnym. Trafiają do Google (GA4) i Datadog, gdzie dostęp mają osoby spoza procesu rekrutacji. Ryzyko: ujawnienie, ponowne użycie tokenu (JWT ważny rok).
- **RODO — kontekst danych:** strona dotyczy testu psychometrycznego; nagrywanie sesji (Session Replay) w tym kontekście może zwiększać ryzyko przetwarzania danych o charakterze oceniającym kandydata.
- **RODO — przekazanie poza EOG:** GA4 i Google Fonts (`fonts.gstatic.com`) łączą się z serwerami Google; Datadog działa w regionie EU (`datadoghq.eu`). Do potwierdzenia w polityce prywatności i umowach powierzenia.
- **RODO — obowiązek informacyjny (art. 13):** na audytowanym widoku brak linku do polityki prywatności i informacji o administratorze. Ograniczenie: sprawdzono tylko widok nieaktywnego linku.

## 10. E-commerce — zgodność z wytycznymi Google

Pushe `ecommerce` w dataLayer porównane z [referencją zdarzeń GA4](https://developers.google.com/analytics/devguides/collection/ga4/reference/events) i [wdrożeniem przez GTM](https://developers.google.com/analytics/devguides/collection/ga4/ecommerce?client_type=gtm). Audyt pasywny widzi tylko zdarzenia odpalane bez interakcji (np. `view_item_list`, `view_item`, `view_promotion`).

Nie dotyczy — strona nie prowadzi sprzedaży.

## Dowody

Plansze generowane z przechwyconego ruchu (HAR): adres strony, czas wysłania, numer wpisu w `raw/<przebieg>/network.har`, parametry żądania z podświetlonymi danymi.

- `screenshots/00-strona.png` — strona i adres (przebieg A)
- `screenshots/E01-A-datadog-rum-logs.png` — Datadog RUM / Logs otrzymuje: JWT, token z URL
- `screenshots/E02-A-google-analytics-4.png` — Google Analytics 4 otrzymuje: token z URL
- `screenshots/E03-A-datadog-session-replay.png` — Datadog Session Replay wysyła dane przed jakąkolwiek zgodą
