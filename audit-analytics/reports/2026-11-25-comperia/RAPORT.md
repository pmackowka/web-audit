# Audyt analityki i prywatności — comperia

- Data: 2026-11-25
- Adres: `https://www.comperia.pl/`
- **Wynik prywatności i zgód: 52/100** (przed zgodą −40, Consent Mode −8) — liczony skryptem z ruchu sieciowego; porównywalny między domenami, 100 = brak śledzenia bez zgody.
- Metoda: pasywna — trzy wczytania strony w świeżej przeglądarce (Chromium, pl-PL, 1440×900): A bez interakcji, B po „odrzuć”, C po „akceptuj”. Bez logowania, formularzy i skanowania.
- Tokeny z URL i dane osobowe są zamaskowane (`abcd…`).

## 1. Podsumowanie — 5 najważniejszych znalezisk

| # | Znalezisko | Waga | Poprawka | Dowód |
|---|---|---|---|---|
| 1 | GA4 (G-W5F1ZMB9NF) wysyła `page_view` z `gcs=G101` (analytics_storage granted) i zapisuje `_ga`, `_ga_W5F1ZMB9NF` przed decyzją użytkownika; w dataLayer brak `consent default`. | wysoka | Dodaj `consent default` z `ad_storage`, `ad_user_data`, `ad_personalization`, `analytics_storage` = denied przed ładowaniem GTM (szablon Cookiebot CMP w GTM, trigger Consent Initialization). | E05, sekcja 2 i 4 |
| 2 | Klasyczny `ga.js` (`ssl.google-analytics.com/r/__utm.gif`, ciasteczka `__utma/__utmb/__utmz`) ładuje się poza GTM w każdym przebiegu ok. 0,5 s po wejściu, także w B przed kliknięciem „Nie wyrażam zgody”. | wysoka | Usuń `ga.js` z kodu strony — pomiar i tak realizuje GA4 w GTM. | E01, sekcja 6–7 |
| 3 | Banery z własnego adservera `ads.comperia.pl` wywołują 18–20 pikseli `ad.doubleclick.net/ddm/trackimp` (Campaign Manager 360) przed jakąkolwiek zgodą; ciasteczko `OAID` (365 dni) w każdym przebiegu. | wysoka | Wstrzymaj ładowanie stref reklamowych do zgody marketingowej (Cookiebot `data-cookieconsent="marketing"`) albo usuń trackery impresji z kreacji. | E03, sekcja 6–7 |
| 4 | Hotjar (2194203), Meta Pixel (`fbevents.js`, `_fbp` w A), Gemius (`redot.gif`, `Gdyn` 395 dni) i własny skrypt `sce.comperiaraty.pl` (`sceuid` 365 dni) ładują się i zapisują identyfikatory przed decyzją; identyfikatory Gemius i `sceuid` zostają po odrzuceniu. | wysoka | Oznacz skrypty kategorią Cookiebot (auto-blocking) albo przenieś je do GTM z warunkiem zgody. | E02, E04, sekcja 6–7 |
| 5 | Po „Nie wyrażam zgody” GA4 wysyła `scroll` z `gcs=G100` (ping bez ciasteczek — tryb zaawansowany), ale `_ga` zapisane wcześniej zostaje w przeglądarce. | średnia | Po naprawie pkt 1 problem znika; do tego czasu nie licz B jako ruchu bez identyfikatora. | E06, sekcja 2 |

## Przebiegi

| Przebieg | Kliknięto | Przycisk „odrzuć” | Przycisk „akceptuj” | Żądania |
|---|---|---|---|---|
| A | — | Nie wyrażam zgody (Cookiebot: #CybotCookiebotDialogBodyButtonDecline) | Akceptuję wszystkie zgody (Cookiebot: #CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll) | 187 |
| B | Nie wyrażam zgody | Nie wyrażam zgody (Cookiebot: #CybotCookiebotDialogBodyButtonDecline) | Akceptuję wszystkie zgody (Cookiebot: #CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll) | 190 |
| C | Akceptuję wszystkie zgody | Nie wyrażam zgody (Cookiebot: #CybotCookiebotDialogBodyButtonDecline) | Akceptuję wszystkie zgody (Cookiebot: #CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll) | 191 |

## 2. Zgody

- CMP: Cookiebot; IAB TCF (`__tcfapi`): nie.

**Tryb Consent Mode (automatycznie): zaawansowany z błędem stanu domyślnego**

| Kontrola | Wynik | Waga |
|---|---|---|
| Stan przed zgodą (A) | GA4 wysyła `analytics_storage` granted przed decyzją użytkownika | wysoka |
| `consent default` | nie wykryto w dataLayer | średnia |

**Komendy `gtag('consent', …)` w dataLayer**

| Przebieg | Komenda |
|---|---|
| B | ["consent", "update", {"ad_storage": "denied", "ad_user_data": "denied", "ad_personalization": "denied", "analytics_storage": "denied", "functionality_storage": "denied", "personalization_storage": "denied", "security_storage": "granted"}] |
| C | ["consent", "update", {"ad_storage": "granted", "ad_user_data": "granted", "ad_personalization": "granted", "analytics_storage": "granted", "functionality_storage": "granted", "personalization_storage": "granted", "security_storage": "granted"}] |

**Parametry Consent Mode w żądaniach GA4** (faza = przed/po kliknięciu w baner)

| Przebieg | Faza | gcs | gcd | Zdarzenia GA4 |
|---|---|---|---|---|
| A | przed | G101 | 13p3t3p2p5l1 | 2 |
| B | przed | G101 | 13p3t3p2p5l1 | 1 |
| B | po | G100 | 13q3u3q2q5l1 | 1 |
| C | przed | G101 | 13p3t3p2p5l1 | 1 |
| C | po | G111 | 13r3v3r2r5l1 | 1 |

**Żądania narzędzi śledzących/monitorujących**

| Przebieg | Faza | Narzędzie × żądania |
|---|---|---|
| A | przed | Google DoubleClick / Floodlight ×18; Hotjar ×5; Google Analytics ×2; Meta Pixel ×2; Google Analytics 4 ×2; Google Tag Manager ×1; Google tag (gtag.js) ×1 |
| B | przed | Google DoubleClick / Floodlight ×20; Hotjar ×4; Google Analytics ×2; Meta Pixel ×2; Google Tag Manager ×1; Google tag (gtag.js) ×1; Google Analytics 4 ×1 |
| B | po | Google Analytics 4 ×1 |
| C | przed | Google DoubleClick / Floodlight ×18; Hotjar ×4; Google Analytics ×2; Meta Pixel ×2; Google Tag Manager ×1; Google tag (gtag.js) ×1; Google Analytics 4 ×1 |
| C | po | Google Ads ×1; Google DoubleClick / Floodlight ×1; Google Analytics 4 ×1 |

**Ocena:** Cookiebot nie blokuje tagów przed decyzją. W fazie „przed” wszystkich trzech przebiegów odpalają GA4, `ga.js`, DoubleClick (trackery impresji z banerów `ads.comperia.pl`), Hotjar, Meta Pixel (ładowanie `fbevents.js` i konfiguracji; żądania `facebook.com/tr` nie zarejestrowano), Gemius i Google tag `ccm/collect` (`pagead2.googlesyndication.com`). Tryb wyznaczony przez kod potwierdzony w `raw/`: dataLayer w A zawiera tylko `gtm.js`, `set developer_id`, `gtm.dom`, `gtm.load` — brak `consent default`, a GA4 i tak wysyła `gcs=G101`. `update` po akceptacji (C) ustawia wszystkie parametry na granted i `gcs` zmienia się na `G111`; po odrzuceniu (B) — `G100`. Kliknięcie w baner uruchamia w GTM ok. 280 triggerów naraz (`gtm.triggers` w `gtm.click`), co wskazuje na przerośnięty kontener.

## 3. Tagi

| Typ | Identyfikatory |
|---|---|
| GA4 | G-W5F1ZMB9NF |
| GTM | GTM-NL4RFW |
| Hotjar | 2194203 |
| LinkedIn | 1319464 |

- Wczytania skryptów GTM/gtag w przebiegu A: GTM-NL4RFW ×1, G-W5F1ZMB9NF ×1.
- `page_view` na identyfikator GA4 w przebiegu A: G-W5F1ZMB9NF ×1.
- Server-side GTM / własny endpoint: nie wykryto.

- Globalne obiekty (A): cookiebot, fbq, hj.
- Narzędzia wg żądań (wszystkie przebiegi): Google DoubleClick / Floodlight ×57; Cookiebot ×18; Hotjar ×13; CDN ×6; Google Analytics ×6; Meta Pixel ×6; Google Analytics 4 ×6; Google Fonts ×3; Google Tag Manager ×3; Google tag (gtag.js) ×3; Google Ads ×1.

## 4. GA4 — żądania collect

Zdarzenia: A: page_view ×1, A: scroll ×1, B: page_view ×1, B: scroll ×1, C: page_view ×1, C: user_engagement ×1

| Przebieg | Faza | t [s] | en | tid | cid | sid | dl | dr | gcs | gcd | ep./up. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | przed | 4.65 | page_view | G-W5F1ZMB9NF | 1283249503.1795592958 | 1795592955 | https://www.comperia.pl/ | — | G101 | 13p3t3p2p5l1 | — |
| A | przed | 18.924 | scroll | G-W5F1ZMB9NF | 1283249503.1795592958 | 1795592955 | https://www.comperia.pl/ | — | G101 | 13p3t3p2p5l1 | {"epn.percent_scrolled": "90"} |
| B | przed | 3.427 | page_view | G-W5F1ZMB9NF | 1106615124.1795592976 | 1795592974 | https://www.comperia.pl/ | — | G101 | 13p3t3p2p5l1 | — |
| B | po | 16.275 | scroll | G-W5F1ZMB9NF | 6753495.1795592989 | 1795592989 | https://www.comperia.pl/ | — | G100 | 13q3u3q2q5l1 | {"epn.percent_scrolled": "90"} |
| C | przed | 4.645 | page_view | G-W5F1ZMB9NF | 1836351271.1795592999 | 1795592996 | https://www.comperia.pl/ | — | G101 | 13p3t3p2p5l1 | — |
| C | po | 16.513 | user_engagement | G-W5F1ZMB9NF | 1836351271.1795592999 | 1795592996 | https://www.comperia.pl/ | — | G111 | 13r3v3r2r5l1 | — |

## 5. Wycieki danych do zewnętrznych hostów

Szukane: token z URL, e-maile, telefony — w URL żądania, nagłówku Referer i body.

_brak_

## 6. Odbiorcy danych

Hosty spoza domeny `www.comperia.pl`. Liczby = żądania w przebiegach A/B/C.

| Host | Firma / narzędzie | A | B | C | Jakie dane |
|---|---|---|---|---|---|
| ad.doubleclick.net | Google / Google DoubleClick / Floodlight | 18 | 20 | 19 | Referer ze stroną |
| sce.comperiaraty.pl | Comperia (domena polityki prywatności) / skrypt `sce` | 6 | 7 | 7 | Referer ze stroną, URL strony w parametrach/body |
| consent.cookiebot.com | Usercentrics / Cookiebot | 2 | 4 | 4 | Referer ze stroną, URL strony w parametrach/body |
| static.hotjar.com | Hotjar / Contentsquare / Hotjar | 3 | 3 | 3 | Referer ze stroną |
| gde-default.hit.gemius.pl | Gemius / Gemius | 3 | 2 | 3 | Referer ze stroną |
| consentcdn.cookiebot.com | Usercentrics / Cookiebot | 2 | 3 | 3 | Referer ze stroną |
| cdn.jsdelivr.net | — / CDN | 2 | 2 | 2 | Referer ze stroną |
| ssl.google-analytics.com | Google / Google Analytics | 2 | 2 | 2 | Referer ze stroną, URL strony w parametrach/body |
| www.googletagmanager.com | Google / Google Tag Manager | 2 | 2 | 2 | Referer ze stroną |
| connect.facebook.net | Meta / Meta Pixel | 2 | 2 | 2 | Referer ze stroną, URL strony w parametrach/body |
| region1.google-analytics.com | Google / Google Analytics | 2 | 2 | 2 | Referer ze stroną, URL strony w parametrach/body, cid/sid (identyfikatory GA) |
| content.hotjar.io | Hotjar / Contentsquare / Hotjar | 2 | 1 | 1 | Referer ze stroną, URL strony w parametrach/body |
| fonts.googleapis.com | Google / Google Fonts | 1 | 1 | 1 | Referer ze stroną |
| pagead2.googlesyndication.com | Google / Google tag (`ccm/collect`) | 1 | 1 | 1 | Referer ze stroną, URL strony w parametrach/body |
| www.google.com | Google / Google Ads | 0 | 0 | 1 | Referer ze stroną, URL strony w parametrach/body |

## 7. Ciasteczka i storage

Narzędzie przypisane heurystycznie po nazwie ciasteczka.

| Nazwa | Domena | Ważność | Narzędzie | A | B | C |
|---|---|---|---|---|---|---|
| CookieConsent | www.comperia.pl | 365 dni | Cookiebot | — | ✔ | ✔ |
| Gdyn | .hit.gemius.pl | 395 dni | Gemius | ✔ | ✔ | ✔ |
| Gdynp | .hit.gemius.pl | 395 dni | Gemius | ✔ | ✔ | ✔ |
| Gtest | .hit.gemius.pl | 7 dni | Gemius | — | ✔ | — |
| OAID | ads.comperia.pl | 365 dni | ? | ✔ | ✔ | ✔ |
| PHPSESSID | www.comperia.pl | 365 dni | ? | ✔ | ✔ | ✔ |
| __cf_bm | .www.cookiebot.com | 0.5 h | Cloudflare | ✔ | — | — |
| __utma | .comperia.pl | 400 dni | Google Analytics (ga.js) | ✔ | — | ✔ |
| __utmb | .comperia.pl | 0.5 h | Google Analytics (ga.js) | ✔ | — | ✔ |
| __utmc | .comperia.pl | sesja | Google Analytics (ga.js) | ✔ | — | ✔ |
| __utmt | .comperia.pl | 0.1 h | Google Analytics (ga.js) | ✔ | — | ✔ |
| __utmz | .comperia.pl | 182 dni | Google Analytics (ga.js) | ✔ | — | ✔ |
| _cs_c | .comperia.pl | 395 dni | ? | ✔ | ✔ | ✔ |
| _cs_ex | .comperia.pl | 30 dni | ? | — | ✔ | ✔ |
| _cs_id | .comperia.pl | 395 dni | ? | ✔ | — | — |
| _cs_s | .comperia.pl | 0.5 h | ? | ✔ | — | — |
| _fbp | .comperia.pl | 90 dni | Meta | ✔ | — | ✔ |
| _ga | .comperia.pl | 400 dni | Google Analytics 4 | ✔ | ✔ | ✔ |
| _ga_W5F1ZMB9NF | .comperia.pl | 400 dni | Google Analytics 4 | ✔ | ✔ | ✔ |
| _gcl_au | .comperia.pl | 90 dni | Google Ads (Conversion Linker) | — | — | ✔ |
| accept | www.comperia.pl | 24.0 h | ? | ✔ | — | — |
| c_s_c_l | s.comperia.pl | 400 dni | ? | ✔ | ✔ | ✔ |
| c_s_c_s | s.comperia.pl | sesja | ? | ✔ | ✔ | ✔ |
| c_s_c_s | www.comperia.pl | sesja | ? | ✔ | ✔ | ✔ |
| c_s_m_x | s.comperia.pl | sesja | ? | ✔ | ✔ | ✔ |
| c_s_m_x | www.comperia.pl | sesja | ? | ✔ | ✔ | ✔ |
| receive-cookie-deprecation | .hit.gemius.pl | 395 dni | Gemius | ✔ | ✔ | ✔ |
| sceuid | .sce.comperiaraty.pl | 365 dni | skrypt `sce` | ✔ | ✔ | ✔ |
| sceuidjs | www.comperia.pl | 365 dni | skrypt `sce` | ✔ | ✔ | ✔ |

Klucze localStorage: _gcl_ls, lastExternalReferrer, lastExternalReferrerTime, sceuidjs.  
Klucze sessionStorage: brak.

## 8. Polityka prywatności i administrator danych

- Linki o prywatności/cookies na stronie: 16.
- Strona wprost wskazuje administratora danych: nie znaleziono.

| Tekst linku | URL | HTTP | Wzmianka o administratorze |
|---|---|---|---|
| Cookiebot od Usercentrics - otwiera się w nowym oknie | https://www.cookiebot.com/en/what-is-behind-powered-by-cookiebot/?utm_source=banner_cb&utm_medium=referral&utm_content=v2 | 200 | False |
| O plikach cookies | https://www.comperia.pl/# | 200 | False |
| Polityka prywatności | https://comperiaraty.pl/polityka-prywatnosci/ | 200 | True |

## 9. Wnioski: RODO i art. 399 Prawa komunikacji elektronicznej

- Fakt: przed decyzją w banerze strona zapisuje w urządzeniu identyfikatory analityczne i reklamowe (`_ga`, `__utma`, `_fbp`, `Gdyn`, `OAID`, `sceuid`) i wysyła dane do Google, Meta, Hotjar i Gemius. Baner sam informuje, że zgoda jest wymagana „przed rozpoczęciem korzystania ze strony” (zrzut 00). Ryzyko: rozbieżność między treścią banera a działaniem strony może być uznana za brak zgody wymaganej przez art. 399 PKE.
- Fakt: po odrzuceniu zgód w przeglądarce zostają `Gdyn`, `Gdynp` (395 dni), `OAID`, `sceuid`, `_ga` (400 dni). Ryzyko: decyzja „Nie wyrażam zgody” może nie być respektowana dla części narzędzi.
- Fakt: strona porównuje kredyty i lokaty, a URL i tytuł strony trafiają do Google, Meta i Hotjar przed zgodą. Ryzyko: kontekst finansowy może zwiększać wagę ewentualnego zarzutu profilowania bez podstawy prawnej.
- Fakt: na stronie głównej nie znaleziono wskazania administratora danych; wskazuje go polityka prywatności na innej domenie (`comperiaraty.pl`). Ryzyko: obowiązek informacyjny z art. 13 RODO może być uznany za utrudniony.

## 10. E-commerce — zgodność z wytycznymi Google

Pushe `ecommerce` w dataLayer porównane z [referencją zdarzeń GA4](https://developers.google.com/analytics/devguides/collection/ga4/reference/events) i [wdrożeniem przez GTM](https://developers.google.com/analytics/devguides/collection/ga4/ecommerce?client_type=gtm). Audyt pasywny widzi tylko zdarzenia odpalane bez interakcji (np. `view_item_list`, `view_item`, `view_promotion`).

Przebieg C, strony: `https://www.comperia.pl/`.

Nie dotyczy — strona nie prowadzi sprzedaży.

## Dowody

Plansze generowane z przechwyconego ruchu (HAR): adres strony, czas wysłania, numer wpisu w `raw/<przebieg>/network.har`, parametry żądania z podświetlonymi danymi.

- `screenshots/00-strona.png` — strona i adres (przebieg A)
- `screenshots/E01-A-google-analytics.png` — Google Analytics wysyła dane przed jakąkolwiek zgodą
- `screenshots/E02-A-hotjar.png` — Hotjar wysyła dane przed jakąkolwiek zgodą
- `screenshots/E03-A-google-doubleclick-floodlight.png` — Google DoubleClick / Floodlight wysyła dane przed jakąkolwiek zgodą
- `screenshots/E04-A-meta-pixel.png` — Meta Pixel wysyła dane przed jakąkolwiek zgodą
- `screenshots/E05-A-google-analytics-4.png` — Google Analytics 4 wysyła dane przed jakąkolwiek zgodą
- `screenshots/E06-B-google-analytics-4.png` — Google Analytics 4 wysyła dane po odrzuceniu zgód
