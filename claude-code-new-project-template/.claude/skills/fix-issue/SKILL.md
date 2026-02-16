---
name: fix-issue
description: Fix a GitHub issue following project standards
argument-hint: [issue-number]
allowed-tools: Bash, Read, Grep, Glob, Edit, Write
---

# Fix GitHub Issue

Fix GitHub issue **#$ARGUMENTS** following project coding standards.

## Process

### 1. Understand the Issue

```bash
gh issue view $ARGUMENTS
```

- Read the issue description carefully
- Understand the expected behavior
- Note any reproduction steps
- Check for related issues or PRs

### 2. Locate Relevant Code

- Search codebase for relevant files using Glob and Grep
- Identify files that need modification
- Read existing code to understand context
- Check for existing tests related to this functionality

### 3. Implement the Fix

- Make necessary code changes following project style
- Keep changes minimal and focused
- Add comments for complex logic
- Ensure code is readable and maintainable

### 4. Add/Update Tests

- Write tests that verify the fix works
- Ensure tests cover edge cases
- Run tests to verify they pass:
  ```bash
  npm run test
  ```

### 5. Verify the Fix

- Run the application locally
- Test the specific functionality that was broken
- Ensure no regressions in related features
- Run linter:
  ```bash
  npm run lint
  ```

### 6. Create Commit

- Create a descriptive commit message:
  - First line: Short summary (50 chars max)
  - Blank line
  - Detailed explanation if needed
  - Reference issue: "Fixes #$ARGUMENTS"

### 7. Summary

Provide a summary:
- What was the root cause?
- What changes were made?
- How was it tested?
- Any follow-up work needed?

---

**Usage**: `/fix-issue 123`
