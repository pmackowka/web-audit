---
name: audit
description: Deterministyczny audyt SEO i dostępności (Lighthouse 0–100 + axe-core) jednej strony pod podanym URL-em. Użyj, gdy użytkownik wpisze /audit <url> albo poprosi o audyt SEO lub dostępności konkretnego adresu.
argument-hint: <url>
disable-model-invocation: true
---

Uruchom dokładnie jedno polecenie:

`npm run audit -s -- $ARGUMENTS`

Ocena strony jest w kodzie (`audit/`), nie po Twojej stronie. Nie interpretuj, nie streszczaj i nie poprawiaj raportu.
Odpowiedz dwiema liniami z wyjścia polecenia: ścieżką raportu i linią statusu. Kod wyjścia: 0 = PASS, 1 = FAIL (są błędy), 2 = audyt się nie wykonał — wtedy pokaż komunikat błędu.
