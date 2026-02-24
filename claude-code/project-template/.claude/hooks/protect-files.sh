#!/bin/bash
#
# Hook: PreToolUse (Edit|Write)
# Purpose: Protect sensitive files from being edited
#

# Read hook input from stdin
INPUT=$(cat)

# Extract file path from tool input
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# If no file path, allow (might be a different tool)
if [ -z "$FILE_PATH" ]; then
  exit 0
fi

# Protected patterns (files that should never be edited)
PROTECTED_PATTERNS=(
  ".env"
  ".env.local"
  ".env.production"
  "*.secret"
  "*.key"
  "*.pem"
  "*credentials*"
  "*secrets*"
  "package-lock.json"
  "pnpm-lock.yaml"
  "yarn.lock"
)

# Check if file matches any protected pattern
for pattern in "${PROTECTED_PATTERNS[@]}"; do
  if [[ "$FILE_PATH" == *"$pattern"* ]]; then
    echo "🚫 BLOCKED: Cannot edit protected file: $FILE_PATH" >&2
    echo "This file matches protected pattern: $pattern" >&2
    echo "" >&2
    echo "If you need to edit this file:" >&2
    echo "1. Edit it manually outside Claude Code" >&2
    echo "2. Or modify .claude/hooks/protect-files.sh to remove this restriction" >&2
    exit 2  # Exit code 2 blocks the action
  fi
done

# Allow the action
exit 0
