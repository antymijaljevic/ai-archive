#!/bin/bash
#
# Hook: PreToolUse (Bash when command contains "git commit")
# Purpose: Validate commit messages follow conventions
#

# Read hook input from stdin
INPUT=$(cat)

# Extract bash command from tool input
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Only check git commit commands
if [[ ! "$COMMAND" =~ git\ commit ]]; then
  exit 0
fi

# Extract commit message from command
# This is a simplified check - adjust based on your needs
if [[ "$COMMAND" =~ -m[[:space:]]+[\"\'](.*)[\"\'"] ]]; then
  COMMIT_MSG="${BASH_REMATCH[1]}"

  # Check commit message length (first line should be < 72 chars)
  FIRST_LINE=$(echo "$COMMIT_MSG" | head -n1)
  LENGTH=${#FIRST_LINE}

  if [ "$LENGTH" -gt 72 ]; then
    echo "🚫 BLOCKED: Commit message first line too long ($LENGTH chars, max 72)" >&2
    echo "Message: $FIRST_LINE" >&2
    exit 2
  fi

  # Check for conventional commit format (optional)
  # Uncomment to enforce: feat:, fix:, chore:, docs:, etc.
  # if [[ ! "$FIRST_LINE" =~ ^(feat|fix|docs|style|refactor|test|chore|perf)(\(.+\))?:\ .+ ]]; then
  #   echo "🚫 BLOCKED: Commit message doesn't follow conventional format" >&2
  #   echo "Expected format: type(scope): description" >&2
  #   echo "Examples:" >&2
  #   echo "  feat(auth): add login functionality" >&2
  #   echo "  fix(api): handle null user error" >&2
  #   echo "  docs: update README" >&2
  #   exit 2
  # fi
fi

exit 0
