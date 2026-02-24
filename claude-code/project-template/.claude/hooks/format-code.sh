#!/bin/bash
#
# Hook: PostToolUse (Edit|Write)
# Purpose: Auto-format code files after editing
#

# Read hook input from stdin
INPUT=$(cat)

# Extract file path from tool input
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# If no file path, skip
if [ -z "$FILE_PATH" ]; then
  exit 0
fi

# Only format code files
if [[ "$FILE_PATH" =~ \.(ts|tsx|js|jsx|json|css|scss|md)$ ]]; then
  # Check if prettier is available
  if command -v npx &> /dev/null; then
    echo "📝 Formatting: $FILE_PATH" >&2

    # Run prettier
    npx prettier --write "$FILE_PATH" 2>&1 | grep -v "Warning" || true

    echo "✓ Formatted successfully" >&2
  fi
fi

exit 0
