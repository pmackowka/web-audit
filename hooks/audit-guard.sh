#!/bin/bash
# PreToolUse agenta `auditor`. Model może tylko uruchomić audyt i zapisać ocenę audit-seo/reports/*.review.md.
# Raport i kod audytu powstają deterministycznie — blokada edycji chroni je przed zmianą przez model.
input=$(cat)
tool=$(jq -r '.tool_name // ""' <<<"$input")

case "$tool" in
  Bash)
    cmd=$(jq -r '.tool_input.command // ""' <<<"$input")
    # Dokładnie jedno polecenie: npm --prefix audit-seo run audit -s -- <url>, bez łączenia komend, przekierowań i podstawień.
    allowed='^npm --prefix audit-seo run audit -s -- https?://[^[:space:];&|`$<>()]+$'
    if [[ "$cmd" =~ $allowed ]]; then exit 0; fi
    echo "Zablokowane: agent auditor może uruchomić tylko 'npm --prefix audit-seo run audit -s -- <url>'." >&2
    exit 2
    ;;
  Write|Edit)
    path=$(jq -r '.tool_input.file_path // ""' <<<"$input")
    if [[ "$path" =~ /audit-seo/reports/[^/]+\.review\.md$ ]]; then exit 0; fi
    echo "Zablokowane: wolno zapisać tylko audit-seo/reports/<raport>.review.md. Raportu i kodu audytu nie zmieniaj." >&2
    exit 2
    ;;
esac
exit 0
