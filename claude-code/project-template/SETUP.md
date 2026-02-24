# Setup Instructions

Quick guide to set up this Claude Code project template.

## Step 1: Copy Template

```bash
# Copy this template to your new project
cp -r claude-code-new-project-template my-new-project
cd my-new-project
```

## Step 2: Customize CLAUDE.md

Edit `CLAUDE.md` with your project information:

```bash
# Open in your editor
code CLAUDE.md
# or
vim CLAUDE.md
```

Update:
- Project name
- Languages and frameworks
- Commands (dev, build, test, etc.)
- Code style preferences
- Architecture decisions
- Git workflow
- Environment variables

## Step 3: Configure Settings

Edit `.claude/settings.json` for team settings:

```bash
code .claude/settings.json
```

Important settings to review:
- **permissions.allow** - Auto-approved commands
- **permissions.deny** - Blocked commands/files
- **permissions.ask** - Commands requiring confirmation
- **hooks** - Automated scripts
- **attribution** - Commit/PR attribution

## Step 4: Set Up Personal Overrides (Optional)

Edit `CLAUDE.local.md` for your personal preferences:

```bash
code CLAUDE.local.md
```

Edit `.claude/settings.local.json` for personal settings:

```bash
code .claude/settings.local.json
```

These files are gitignored and won't be shared with your team.

## Step 5: Configure MCP Servers (Optional)

If you need external integrations (GitHub, databases, etc.):

### Option A: Use CLI
```bash
# Add GitHub integration
claude mcp add --transport http --scope project github https://mcp.github.com

# Add PostgreSQL
claude mcp add --transport stdio --scope project \
  --env DATABASE_URL=$DATABASE_URL postgres \
  -- npx -y @modelcontextprotocol/server-postgres
```

### Option B: Edit .mcp.json directly
```bash
code .mcp.json
```

## Step 6: Review Skills

Check the example skills in `.claude/skills/`:
- **deploy** - Deployment workflow
- **fix-issue** - Fix GitHub issues
- **review-pr** - Code review workflow

Customize or remove as needed:

```bash
# Remove a skill
rm -rf .claude/skills/deploy

# Add your own
mkdir .claude/skills/my-skill
code .claude/skills/my-skill/SKILL.md
```

## Step 7: Review Subagents

Check example subagents in `.claude/agents/`:
- **code-reviewer** - Automated code review
- **debugger** - Debug errors
- **security-checker** - Security audit

Customize or remove as needed:

```bash
# Test a subagent
/agents
# Use the interactive menu to test your agents
```

## Step 8: Review Modular Rules

Check rules in `.claude/rules/`:
- **code-style.md** - Code style conventions
- **testing.md** - Testing requirements
- **security.md** - Security rules
- **api/conventions.md** - API-specific rules

Edit or add new rules as needed.

## Step 9: Test Hooks

Hooks are in `.claude/hooks/`:
- **protect-files.sh** - Block editing sensitive files
- **format-code.sh** - Auto-format after edits
- **validate-commit.sh** - Validate commit messages

Test them:

```bash
# Make sure they're executable
chmod +x .claude/hooks/*.sh

# Test protect-files hook by trying to edit .env
# (should be blocked)

# Test format-code by editing a file
# (should auto-format)
```

## Step 10: Set Up Environment

```bash
# Copy example env file
cp .env.example .env

# Fill in your values
code .env
```

## Step 11: Initialize Git

```bash
# Initialize git if not already
git init

# Verify .gitignore is working
git status

# Should NOT show:
# - CLAUDE.local.md
# - .claude/settings.local.json
# - .env

# First commit
git add .
git commit -m "Initial commit with Claude Code configuration"
```

## Step 12: Test Configuration

Run Claude Code to verify everything works:

```bash
cd my-new-project
claude

# Test that memory is loaded
> What commands can I run in this project?

# Test permissions
> Run npm test

# Test MCP servers
/mcp

# Test agents
/agents

# Check for issues
/doctor
```

## Optional: Clean Up Template Files

Remove template-specific files you don't need:

```bash
# Remove setup instructions
rm SETUP.md

# Remove this README if you want to write your own
rm README.md
```

## Quick Configuration Checklist

- [ ] Copied template to new project
- [ ] Updated `CLAUDE.md` with project info
- [ ] Configured `.claude/settings.json` permissions
- [ ] Set up personal `CLAUDE.local.md` (optional)
- [ ] Added MCP servers if needed
- [ ] Reviewed and customized skills
- [ ] Reviewed and customized agents
- [ ] Reviewed and customized rules
- [ ] Tested hooks
- [ ] Created `.env` from `.env.example`
- [ ] Initialized git repository
- [ ] Verified `.gitignore` is working
- [ ] Tested Claude Code configuration

## Troubleshooting

### Hooks not running
```bash
# Make sure they're executable
chmod +x .claude/hooks/*.sh

# Check hook configuration in settings.json
code .claude/settings.json
```

### MCP servers not working
```bash
# Check server status
/mcp

# Re-authenticate if needed
/mcp
# Then follow the authentication flow
```

### Memory not loading
```bash
# Verify file location
ls -la CLAUDE.md
ls -la .claude/CLAUDE.md

# Check for syntax errors
cat CLAUDE.md

# Use /doctor to diagnose
/doctor
```

### Agent not responding
```bash
# Check agent configuration
code .claude/agents/my-agent/SKILL.md

# Verify frontmatter is valid YAML
# Verify 'name' and 'description' fields exist
```

## Next Steps

1. Share with your team via git
2. Add more project-specific rules
3. Create custom skills for your workflow
4. Set up CI/CD integration
5. Explore the [official docs](https://docs.claude.com/claude-code)

---

**Need help?** Run `/help` in Claude Code or check the [GitHub issues](https://github.com/anthropics/claude-code/issues)
