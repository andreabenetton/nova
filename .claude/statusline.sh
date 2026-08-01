#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Claude Code status line: model · host · clone-dir · git branch · token usage.
# Surfaces which host + clone + branch the session is on — the
# <hostname>/<clone-dir>/<task> attribution model (CLAUDE.md §Git discipline →
# Concurrent contributors). Reads the session JSON on stdin; runs locally,
# no API tokens. Configured by .claude/settings.json `statusLine`.
#
# Token counts are NOT in the stdin JSON. They are read from the session
# transcript (.transcript_path), whose assistant records each carry a
# `message.usage` object. Assistant records repeat in the JSONL, so they are
# deduplicated by requestId before totalling.
input=$(cat)

dir=$(printf '%s' "$input" | jq -r '.workspace.current_dir // empty')
[ -z "$dir" ] && dir="$PWD"
model=$(printf '%s' "$input" | jq -r '.model.display_name // "Claude"')
host=$(hostname -s 2>/dev/null || hostname 2>/dev/null || echo "?")
clone=$(basename "$dir")
branch=$(git -C "$dir" branch --show-current 2>/dev/null)

printf '[%s] 🖥  %s 📁 %s 🌿 %s' "$model" "$host" "$clone" "${branch:-detached}"

# --- token usage -----------------------------------------------------------
transcript=$(printf '%s' "$input" | jq -r '.transcript_path // empty')
[ -f "$transcript" ] || exit 0

usage=$(jq -rs '
  # one record per assistant request; later duplicates discarded
  ( [ .[] | select(.type == "assistant" and .message.usage != null) ]
    | group_by(.requestId // .uuid)
    | map(.[0].message.usage) ) as $u
  | if ($u | length) == 0 then "" else
      ($u | last) as $l
      | [ ( ($l.input_tokens // 0)
          + ($l.cache_creation_input_tokens // 0)
          + ($l.cache_read_input_tokens // 0) ),
          ( ($l.input_tokens // 0) + ($l.cache_creation_input_tokens // 0) ),
          ( $l.output_tokens // 0 ),
          ( $u | map(.output_tokens // 0) | add ) ]
      | @tsv
    end
' "$transcript" 2>/dev/null)

[ -n "$usage" ] || exit 0
IFS=$'\t' read -r ctx turn_in turn_out sess_out <<<"$usage"

# 12345 -> 12.3k, 900 -> 900
human() {
  if [ "$1" -ge 1000 ] 2>/dev/null; then
    awk -v n="$1" 'BEGIN { printf "%.1fk", n / 1000 }'
  else
    printf '%s' "${1:-0}"
  fi
}

limit=$(printf '%s' "$input" | jq -r 'if .exceeds_200k_tokens then 1000000 else 200000 end')
pct=$(awk -v c="$ctx" -v l="$limit" 'BEGIN { printf "%d", (c * 100) / l }')

printf ' 🧮 %s/%s (%s%%) · ↑%s ↓%s · Σ↓%s' \
  "$(human "$ctx")" "$(human "$limit")" "$pct" \
  "$(human "$turn_in")" "$(human "$turn_out")" "$(human "$sess_out")"
