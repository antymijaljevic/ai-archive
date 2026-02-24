---
name: review-pr
description: Review a pull request for quality and issues
argument-hint: [pr-number]
allowed-tools: Bash, Read, Grep
---

# Pull Request Review

Review PR **#$ARGUMENTS** for code quality, security, and best practices.

## Review Process

### 1. Get PR Context

```bash
gh pr view $ARGUMENTS
gh pr diff $ARGUMENTS
```

- Read PR description and purpose
- Understand what changes are being made
- Check for breaking changes

### 2. Code Quality Review

Check for:

**Readability**
- Clear variable and function names
- Appropriate comments for complex logic
- Consistent code style with project
- No overly complex functions (>50 lines)

**Maintainability**
- DRY principle followed (no duplicated code)
- Proper separation of concerns
- Functions have single responsibility
- Code is testable

**Error Handling**
- Proper error handling and validation
- User-facing errors are clear
- Edge cases are handled
- No silent failures

### 3. Security Review

Check for:
- No exposed secrets or API keys
- Input validation on all user data
- No SQL injection vulnerabilities
- No XSS vulnerabilities
- Authentication/authorization checks
- Sensitive data properly encrypted

### 4. Performance Review

Check for:
- No unnecessary re-renders (React)
- Efficient database queries
- Proper caching where appropriate
- No memory leaks
- Optimized imports (tree-shaking)

### 5. Testing Review

Check for:
- Tests cover new functionality
- Tests cover edge cases
- Tests are clear and maintainable
- Mock data is realistic
- Tests run successfully

```bash
npm run test
```

### 6. Documentation Review

Check for:
- API changes documented
- README updated if needed
- Comments explain "why" not "what"
- Breaking changes clearly noted

### 7. Provide Feedback

Organize feedback by priority:

**🔴 Critical (Must Fix)**
- Security vulnerabilities
- Breaking changes without migration
- Data loss or corruption risks

**🟡 Warnings (Should Fix)**
- Code quality issues
- Missing tests
- Performance concerns
- Inconsistent style

**🟢 Suggestions (Consider)**
- Refactoring opportunities
- Alternative approaches
- Future improvements

### 8. Final Recommendation

- ✅ **Approve**: Code is ready to merge
- 🔄 **Request Changes**: Issues must be addressed
- 💬 **Comment**: Questions or minor suggestions

---

**Usage**: `/review-pr 456`
