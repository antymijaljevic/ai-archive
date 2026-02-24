---
name: deploy
description: Deploy application to specified environment
disable-model-invocation: true
argument-hint: [environment]
allowed-tools: Bash, Read
---

# Deploy Application

Deploy the application to **$ARGUMENTS** environment.

## Pre-Deployment Checks

1. **Verify clean working directory**
   ```bash
   git status
   ```
   - Ensure no uncommitted changes
   - Ensure on correct branch

2. **Run all tests**
   ```bash
   npm run test
   ```
   - ALL tests must pass
   - If any test fails, STOP and report error

3. **Build production bundle**
   ```bash
   npm run build
   ```
   - Verify build succeeds
   - Check for any warnings

4. **Verify environment variables**
   - Check that required env vars are set for $ARGUMENTS
   - Read deployment docs if unsure

## Deployment

5. **Run deployment command**
   ```bash
   npm run deploy:$ARGUMENTS
   ```

6. **Verify deployment**
   - Check health endpoint
   - Verify application is responding
   - Check error logs for issues

7. **Create deployment tag** (for production only)
   ```bash
   git tag -a deploy-$(date +%Y%m%d-%H%M%S) -m "Deployed to $ARGUMENTS"
   git push origin --tags
   ```

## ⚠️ Important

- **ALWAYS ask user for confirmation** before deploying to production
- If deploying to staging, you can proceed without confirmation
- If ANY step fails, STOP immediately and report the error
- Never force-push or skip tests

## Rollback

If deployment fails:
```bash
npm run rollback:$ARGUMENTS
```

---

**Usage**: `/deploy staging` or `/deploy production`
