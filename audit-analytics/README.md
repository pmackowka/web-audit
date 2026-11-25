# audit-analytics

Pasywny audyt wdrożenia analityki i prywatności na stronie WWW: tagi, Consent Mode v2, zgody, ciasteczka, odbiorcy danych, wycieki tokenów i danych osobowych.

## Uruchomienie

```bash
cd audit-analytics
uv sync && uv run playwright install chromium   # raz
uv run audit.py https://example.com --slug example [--extra-url https://example.com/kategoria --extra-url https://example.com/produkt] [--mask "Jan Kowalski"] [--headed]
```

W Claude Code: `/analytics-audit <url> <firma>` — uruchamia skrypt i uzupełnia raport wg [`CLAUDE.md`](CLAUDE.md).

## Co sprawdza

Trzy wczytania strony w świeżym kontekście Chromium (pl-PL, 1440×900):

| Przebieg | Interakcja |
|---|---|
| A | brak — stan przed zgodą |
| B | klik „odrzuć / tylko niezbędne” (pominięty, gdy brak przycisku) |
| C | klik „akceptuj wszystkie” (pominięty, gdy brak przycisku) |

Każdy przebieg: networkidle + 8 s, przewinięcie do dołu, 4 s. Zbierane: HAR z treścią, log żądań z body POST, ciasteczka, localStorage/sessionStorage, `window.dataLayer`.

`--extra-url` dokłada w każdym przebiegu kolejne strony (wejście pod adres, przewinięcie) — potrzebne do walidacji e-commerce, bo strona główna rzadko wysyła zdarzenia produktowe.

Skrypt niczego nie wysyła i nie wypełnia; klika tylko przyciski banera zgód.

## Dowody (`screenshots/`)

- `00-strona.png` — jedyny zrzut strony: pasek adresu (token zamaskowany), czas pierwszego żądania z HAR.
- `E01…png` — plansza na każde znalezisko, w układzie panelu Network: adres strony, czas wysłania, numer wpisu w `raw/<przebieg>/network.har`, General / Query String / Payload z podświetlonymi danymi. Wycieki: jedna plansza na narzędzie (żądanie z najwięcej trafieniami); tagi bez zgody: przebieg A, po odrzuceniu: przebieg B.

Plansze są renderowane z przechwyconego ruchu, a nie zrzucane z DevTools — dzięki temu są powtarzalne i zamaskowane. Weryfikacja: „wpis #n” = n-te żądanie w `raw/<przebieg>/network.har` (liczone od 1); po imporcie HAR do DevTools (Network → Import HAR) szukaj po URL i czasie z planszy.

## Jak czytać raport

`reports/RRRR-MM-DD-<firma>/RAPORT.md` (raport i plansze w repo, `raw/` w `.gitignore`):
- **Wynik prywatności i zgód (nagłówek)** — 0–100 liczony przez `privacy_score()` z ruchu, do porównywania domen: 100 minus kary — narzędzie śledzące przed zgodą 10 pkt (maks. 40), po odrzuceniu 10 pkt (maks. 25; ping GA4 z `analytics_storage` denied bez kary), kontrola Consent Mode wysoka 5 / średnia 3 (maks. 15), host z wyciekiem 10 pkt (maks. 20). Loader GTM/gtag.js bez kary. Strona bez śledzenia ma 100 — wynik mierzy prywatność, nie jakość pomiaru.
- **Faza przed/po** — żądanie wysłane przed/po kliknięciu w baner. Tag analityczny w B/„po” = odpala mimo odmowy.
- **Tryb Consent Mode (sekcja 2)** — [podstawowy](https://developers.google.com/tag-platform/security/concepts/consent-mode): zero żądań GA4 przed zgodą; zaawansowany: przed zgodą idą pingi z `gcs` denied. Kontrole: `consent default` z `ad_storage`, `analytics_storage`, `ad_user_data`, `ad_personalization` (denied), `wait_for_update`, `consent update` po akceptacji, `gcs` po odrzuceniu (B) i akceptacji (C).
- **gcs** — `G1xy`: x = ad_storage, y = analytics_storage (1 granted, 0 denied). `gcd` idzie zawsze, więc nie świadczy o Consent Mode.
- **E-commerce (sekcja 10)** — pushe `ecommerce` w dataLayer vs [referencja zdarzeń GA4](https://developers.google.com/analytics/devguides/collection/ga4/reference/events): format UA zamiast `items`, produkty bez `item_id`/`item_name`, liczby jako tekst, `value` bez `currency`, `value` ≠ suma price×quantity, brak `transaction_id`, brak `ecommerce: null`, zdarzenie bez żądania GA4 albo żądanie GA4 bez produktów (`pr1…`). Walidowany przebieg C (po akceptacji), a bez niego A.
- **Wycieki** — token z URL, e-mail lub telefon w URL, Refererze albo body żądania do obcej domeny.
- Tokeny i dane osobowe w raporcie są zamaskowane (`abcd…`). Surowe dane zostają lokalnie w `raw/` (w `.gitignore`).

