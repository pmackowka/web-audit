#!/bin/bash
# Stop agenta `auditor` (w subagencie działa jako SubagentStop). Sprawdza, czy ocena opiera się na raporcie:
# 1) najnowszy raport ma swój plik .review.md, 2) każde id reguły cytowane w ocenie występuje w raporcie.
# Przy pierwszym niepowodzeniu blokuje zakończenie (exit 2) i każe poprawić; przy kolejnym oznacza ocenę ostrzeżeniem,
# żeby nie wpaść w nieskończoną pętlę.
input=$(cat)
dir="${CLAUDE_PROJECT_DIR:-$(jq -r '.cwd' <<<"$input")}"
retry=$(jq -r '.stop_hook_active // false' <<<"$input")

# Raport tego agenta (przy równoległych audytach najnowszy plik może należeć do innej domeny). Kolejność źródeł:
# końcowa odpowiedź, potem transkrypt subagenta — od Claude Code v2.1.271 raport oddany przez SubagentHandback
# nie trafia do last_assistant_message (https://code.claude.com/docs/en/hooks#subagentstop); na końcu najnowszy plik.
path_re='audit-seo/reports/[a-z0-9.-]+-[0-9]{4}-[0-9]{2}-[0-9]{2}\.md'
named=$(jq -r '.last_assistant_message // ""' <<<"$input" | grep -oE "$path_re" | head -1)
transcript=$(jq -r '.agent_transcript_path // ""' <<<"$input")
if [ -z "$named" ] && [ -f "$transcript" ]; then
  named=$(grep -oE "$path_re" "$transcript" | grep -v '\.review\.md$' | tail -1)
fi
if [ -n "$named" ] && [ -f "$dir/$named" ]; then
  report="$dir/$named"
else
  report=$(ls -t "$dir"/audit-seo/reports/*.md 2>/dev/null | grep -v '\.review\.md$' | head -1)
fi
[ -z "$report" ] && exit 0
review="${report%.md}.review.md"

if [ ! -f "$review" ] || [ "$review" -ot "$report" ]; then
  [ "$retry" = "true" ] && exit 0
  echo "Brak aktualnej oceny. Zapisz ją do ${review#$dir/}." >&2
  exit 2
fi

# Porównanie całych id (zbiory), nie podciągów: „seo-h” nie może przejść dzięki „seo-h1” w raporcie.
ids() { grep -oE '\b(seo|a11y|lh)-[a-z0-9-]+' "$1" | sort -u; }
unknown=$(comm -23 <(ids "$review") <(ids "$report"))
[ -z "$unknown" ] && exit 0

if [ "$retry" = "true" ]; then
  printf '\n> UWAGA (hook check-review): ocena cytuje id spoza raportu: %s\n' "$(echo $unknown)" >> "$review"
  exit 0
fi
echo "Ocena cytuje id, których nie ma w raporcie ${report#$dir/}: $(echo $unknown). Usuń je albo zastąp id z raportu." >&2
exit 2
