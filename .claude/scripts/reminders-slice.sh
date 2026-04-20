#!/usr/bin/env bash
# Fetch a slice of Apple Reminders as JSON via the apple-mcp Swift helper.
# Wraps compound shell logic so the /bs:reminders command is one atomic call
# per invocation (simpler to allow in .claude/settings.json).
#
# Usage:
#   reminders-slice.sh overdue
#   reminders-slice.sh today
#   reminders-slice.sh week
#   reminders-slice.sh flagged
#   reminders-slice.sh list "<list name>"
#   reminders-slice.sh lists              # just the list names
#   reminders-slice.sh everything         # full incomplete set (projected)
#
# Output: JSON array on stdout.

set -euo pipefail

HELPER="$HOME/code/apple-mcp/bin/reminders-helper"
SLICE="${1:-}"

case "$SLICE" in
  overdue)
    TODAY=$(date +%Y-%m-%d)
    "$HELPER" list-reminders --completed incomplete \
      | jq --arg today "$TODAY" '[.[]
          | select(.dueDate != null
                   and (.dueDate | fromdateiso8601 | localtime | strftime("%Y-%m-%d")) < $today)
          | {id, name, listName, dueDate, priority}]'
    ;;
  today)
    TODAY=$(date +%Y-%m-%d)
    "$HELPER" list-reminders --completed incomplete \
      | jq --arg today "$TODAY" '[.[]
          | select(.dueDate != null
                   and (.dueDate | fromdateiso8601 | localtime | strftime("%Y-%m-%d")) == $today)
          | {id, name, listName, dueDate, priority}]'
    ;;
  week)
    TODAY=$(date +%Y-%m-%d)
    END=$(date -v+7d +%Y-%m-%d)
    "$HELPER" list-reminders --completed incomplete \
      | jq --arg today "$TODAY" --arg end "$END" '[.[]
          | select(.dueDate != null
                   and ((.dueDate | fromdateiso8601 | localtime | strftime("%Y-%m-%d")) as $d
                        | $d >= $today and $d <= $end))
          | {id, name, listName, dueDate, priority}]'
    ;;
  flagged)
    "$HELPER" list-reminders --completed incomplete \
      | jq '[.[]
          | select(.priority > 0 and .dueDate == null)
          | {id, name, listName, priority}]'
    ;;
  list)
    LIST_NAME="${2:-}"
    if [ -z "$LIST_NAME" ]; then
      echo "usage: $0 list \"<list name>\"" >&2
      exit 2
    fi
    "$HELPER" list-reminders --completed incomplete --list-name "$LIST_NAME" \
      | jq '[.[] | {id, name, dueDate, priority}]'
    ;;
  lists)
    "$HELPER" list-lists | jq -r '.[].name'
    ;;
  everything)
    "$HELPER" list-reminders --completed incomplete \
      | jq '[.[] | {id, name, listName, dueDate, priority}]'
    ;;
  "")
    echo "usage: $0 {overdue|today|week|flagged|list <name>|lists|everything}" >&2
    exit 2
    ;;
  *)
    echo "unknown slice: $SLICE" >&2
    echo "usage: $0 {overdue|today|week|flagged|list <name>|lists|everything}" >&2
    exit 2
    ;;
esac
