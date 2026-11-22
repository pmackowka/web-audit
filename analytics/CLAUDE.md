# analytics — instrukcje dla Claude Code

Pasywny audyt wdrożenia analityki i prywatności dowolnej strony: tagi, Consent Mode v2, zgody, ciasteczka, odbiorcy danych, wycieki tokenów i danych osobowych, walidacja e-commerce dataLayer. Raport ma dać konkretne, możliwe do poprawy znaleziska.

## Zasady (bezwzględne)
- Kod zmieniaj tylko w `analytics/`; raport powstaje w `reports/analytics/<data>-<firma>/`.
- Audyt pasywny: zachowuj się jak zwykły odwiedzający — wczytanie, przewinięcie, klik w baner zgód. Bez skanowania, fuzzingu, logowania, wypełniania formularzy, zgadywania ścieżek i wielokrotnego odpytywania serwera.
- Nie klikaj przycisków, które rozpoczynają test, wysyłają formularz lub zużywają jednorazowy link. `audit.py` klika wyłącznie przyciski banera zgód (filtr `FORBIDDEN_RE` + wymóg kontenera z tekstem o cookies/zgodach).
- Ręczna weryfikacja w przeglądarce (np. Chrome DevTools) — te same ograniczenia.
- Tokeny z URL i dane osobowe audytującego maskuj w raporcie i na zrzutach (`7ea9…`). `raw/` zawiera dane niezamaskowane.
- `reports/analytics/` jest w `.gitignore` (repo jest publiczne) — raportów nie commituj.

## Procedura
1. `cd analytics && uv sync && uv run playwright install chromium` (tylko przy pierwszym uruchomieniu).
2. `uv run audit.py <url> --slug <firma>`; dane osobowe widoczne na stronie (imię, e-mail) dodaj jako `--mask "<tekst>"`. Sklep internetowy: dodaj `--extra-url` ze stroną kategorii i produktu (adresy z linków na stronie, nie zgadywane); bez nich sekcja 10 będzie pusta.
3. Przeczytaj szkic `reports/analytics/<data>-<firma>/RAPORT.md` i obejrzyj wszystkie plansze z `screenshots/` (`00-strona.png` + `E*.png`); w podsumowaniu odwołuj się do plansz.
   Poprawka analizy bez ponownego wczytywania strony: `uv run audit.py <url> --slug <firma> --rebuild` (nadpisuje RAPORT.md — uzupełnienia rób po ostatnim rebuildzie).
4. Zweryfikuj automatyczne tabele w `raw/<A|B|C>/requests.json`, `datalayer.json`, `cookies.json` — heurystyki (narzędzie po hoście, telefon po wzorcu) mogą się mylić; popraw raport, nie dopisuj nic bez dowodu.
5. Uzupełnij bloki `<!-- DO UZUPEŁNIENIA -->`:
   - **Podsumowanie:** 5 znalezisk, waga (wysoka/średnia/niska), konkretna poprawka, odwołanie do zrzutu/sekcji.
   - **E-commerce (sekcja 10):** strona bez sprzedaży (portal, SaaS, rekrutacja) → zastąp treść sekcji zdaniem „Nie dotyczy — strona nie prowadzi sprzedaży.” i nie używaj `--extra-url`. Sklep → sprawdź każde zgłoszenie w `raw/<C|A>/datalayer.json`; najpoważniejsze problemy przenieś do podsumowania.
   - **Zgody:** czy tagi odpalają przed zgodą (A) i po odrzuceniu (B, faza „po”); czy Consent Mode v2 ma `default` denied i `update` po kliknięciu.
   - **Wnioski RODO / art. 399 PKE** (przechowywanie informacji i dostęp do nich w urządzeniu końcowym — cookies, localStorage): tylko fakty i potencjalne ryzyka, bez kwalifikacji prawnej („może”, „ryzyko”, nigdy „narusza”).
6. Kontrola maskowania: `grep -rn "<pełny token>" reports/analytics/<data>-<firma>/RAPORT.md` musi być pusty; obejrzyj zrzuty pod kątem tokenów i danych osobowych.
7. Testy parserów: `uv run python -m unittest test_audit.py`.
8. Pokaż raport i ścieżkę do folderu raportu.

## Interpretacja
- `gcs=G1xy`: x = ad_storage, y = analytics_storage (1 granted, 0 denied). `gcd` raportuj surowo; litery tylko z potwierdzonego źródła.
- Faza „przed”/„po” = żądanie przed/po kliknięciu w baner w danym przebiegu.
- Żądanie collect GA4 na hoście innym niż Google = server-side GTM lub proxy.
