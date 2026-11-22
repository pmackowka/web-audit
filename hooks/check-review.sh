#!/bin/bash
# Stop agenta `auditor` (w subagencie działa jako SubagentStop). Sprawdza, czy ocena opiera się na raporcie:
# 1) najnowszy raport ma swój plik .review.md, 2) każde id reguły cytowane w ocenie występuje w raporcie.
# Przy pierwszym niepowodzeniu blokuje zakończenie (exit 2) i każe poprawić; przy kolejnym oznacza ocenę ostrzeżeniem,
# żeby nie wpaść w nieskończoną pętlę.
input=$(cat)
dir="${CLAUDE_PROJECT_DIR:-$(jq -r '.cwd' <<<"$input")}"
retry=$(jq -r '.stop_hook_active // false' <<<"$input")

# Raport z końcowej odpowiedzi agenta (przy równoległych audytach najnowszy plik może należeć do innej domeny);
# gdy odpowiedź go nie zawiera — najnowszy raport w reports/.
named=$(jq -r '.last_assistant_message // ""' <<<"$input" | grep -oE 'reports/[a-z0-9.-]+-[0-9]{4}-[0-9]{2}-[0-9]{2}\.md' | head -1)
if [ -n "$named" ] && [ -f "$dir/$named" ]; then
  report="$dir/$named"
else
  report=$(ls -t "$dir"/reports/*.md 2>/dev/null | grep -v '\.review\.md$' | head -1)
fi
[ -z "$report" ] && exit 0
review="${report%.md}.review.md"

if [ ! -f "$review" ] || [ "$review" -ot "$report" ]; then
  [ "$retry" = "true" ] && exit 0
  echo "Brak aktualnej oceny. Zapisz ją do ${review#$dir/}." >&2
  exit 2
fi

unknown=$(grep -oE '\b(seo|a11y|lh)-[a-z0-9-]+' "$review" | sort -u | while read -r id; do
  grep -qF -- "$id" "$report" || echo "$id"
done)
[ -z "$unknown" ] && exit 0

if [ "$retry" = "true" ]; then
  printf '\n> UWAGA (hook check-review): ocena cytuje id spoza raportu: %s\n' "$(echo $unknown)" >> "$review"
  exit 0
fi
echo "Ocena cytuje id, których nie ma w raporcie ${report#$dir/}: $(echo $unknown). Usuń je albo zastąp id z raportu." >&2
exit 2
