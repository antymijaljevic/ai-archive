# How to Use This Template

Quick reference for using this Claude Code project template.

## 🚀 Quick Start

### Option 1: Using the Quick Start Script (Easiest)

```bash
# Run the interactive setup
./quick-start.sh

# Follow the prompts:
# 1. Enter project name
# 2. Choose location
# 3. Initialize git (y/n)
```

### Option 2: Manual Copy

```bash
# Copy template to your new project
cp -r claude-code-new-project-template my-new-project
cd my-new-project

# Remove template-specific files
rm quick-start.sh SETUP.md

# Initialize git
git init
cp .env.example .env
git add .
git commit -m "Initial commit"
```

## 📝 Customize for Your Project

### 1. Update CLAUDE.md

This is the most important file - it tells Claude about your project.

```bash
code CLAUDE.md
```

Update these sections:
- **Project name and quick info**
- **Commands** (dev, build, test, deploy)
- **Code style** preferences
- **Architecture decisions**
- **Git workflow**
- **Environment variables**
- **Common gotchas**

**Example:**
```markdown
# Project: My Awesome App

## Commands
npm run dev      # Start dev server on :3000
npm run test     # Run tests with Vitest
npm run build    # Build for production

## Architecture Decisions
- Using Zustand for state (not Redux - lighter)
- API calls with React Query
- Tests with Vitest (faster than Jest)
```

### 2. Configure Permissions

Edit `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run test)",
      "Bash(npm run lint)"
    ],
    "deny": [
      "Read(.env*)",
      "Bash(rm -rf *)"
    ],
    "ask": [
      "Bash(git push *)",
      "Bash(npm install *)"
    ]
  }
}
```

### 3. Personal Preferences (Optional)

Edit `CLAUDE.local.md` and `.claude/settings.local.json` for personal overrides:

```bash
code CLAUDE.local.md
code .claude/settings.local.json
```

These files are gitignored and won't be shared with your team.

## 🎯 Using Skills (Slash Commands)

Skills are pre-configured workflows you can trigger with `/command`:

### Available Skills

```bash
/deploy [environment]    # Deploy to staging/production
/fix-issue [number]      # Fix a GitHub issue
/review-pr [number]      # Review a pull request
```

### Using Skills

```bash
# In Claude Code
> /deploy staging
> /fix-issue 123
> /review-pr 456
```

### Creating Custom Skills

```bash
mkdir .claude/skills/my-workflow
cat > .claude/skills/my-workflow/SKILL.md << 'EOF'
---
name: my-workflow
description: What this does
disable-model-invocation: true  # Only you can invoke
argument-hint: [arguments]
---

# Workflow instructions here
1. Step one
2. Step two
EOF
```

## 🤖 Using Subagents

Subagents are specialized AI assistants for specific tasks.

### Available Subagents

- **code-reviewer** - Reviews code for quality/security after edits
- **debugger** - Investigates errors and test failures
- **security-checker** - Audits code for security issues

### Using Subagents

#### Automatic (Proactive)
Subagents with good descriptions auto-activate:

```bash
> I made some changes to the auth module
# code-reviewer automatically reviews your changes
```

#### Manual (Request Specific)
```bash
> Use the security-checker agent to audit the API
> Have the debugger investigate this test failure
```

#### Interactive
```bash
/agents
# Browse, test, and manage subagents
```

## 📏 Modular Rules

Rules in `.claude/rules/` are auto-loaded based on context.

### Available Rules

- **code-style.md** - Always active
- **testing.md** - Active for test files
- **security.md** - Active when handling sensitive code
- **api/conventions.md** - Active for API routes only

### Path-Scoped Rules

Rules can target specific files using YAML frontmatter:

```markdown
---
paths:
  - "src/api/**/*.ts"
  - "lib/**/*.js"
---

# Rules only apply to these files
```

## 🪝 Hooks (Automation)

Hooks run automatically at specific events.

### Active Hooks

1. **protect-files.sh** (PreToolUse)
   - Blocks editing `.env`, secrets, lock files

2. **format-code.sh** (PostToolUse)
   - Auto-formats code after editing

3. **validate-commit.sh** (PreToolUse)
   - Validates commit message format

### Testing Hooks

```bash
# Try editing a protected file
> Edit .env file
# Should be blocked by protect-files.sh

# Edit a code file
> Edit src/component.tsx
# Should auto-format after edit
```

### Managing Hooks

```bash
/hooks
# Interactive hook management
```

## 🔌 MCP Servers (External Integrations)

Connect to external services (databases, APIs, tools).

### Available Servers (Example)

- **github** - GitHub integration
- **postgres** - Database queries
- **filesystem** - Extended file access

### Adding MCP Servers

```bash
# Add GitHub
claude mcp add --transport http --scope project \
  github https://mcp.github.com

# Add PostgreSQL
claude mcp add --transport stdio --scope project \
  --env DATABASE_URL=$DATABASE_URL postgres \
  -- npx -y @modelcontextprotocol/server-postgres

# Check status
/mcp
```

### Using MCP Resources

```bash
> Analyze @github:issue://123
> Query @postgres:table://users
> Read @docs:file://api/spec
```

## 🧪 Testing Your Configuration

### Run Doctor

```bash
claude
> /doctor
```

Checks for:
- Configuration errors
- Missing files
- Permission issues
- Hook problems

### Verify Memory Loading

```bash
> What commands can I run in this project?
# Should reference commands from CLAUDE.md
```

### Test Permissions

```bash
> Run npm test
# Should auto-approve (in allow list)

> Push to git
# Should ask for confirmation (in ask list)

> Read .env file
# Should be blocked (in deny list)
```

### Test Skills

```bash
/deploy staging
# Should follow deployment workflow
```

### Test Agents

```bash
> Use code-reviewer to check my recent changes
# Should analyze code and provide feedback
```

## 📦 Sharing with Team

### What to Commit

```bash
git add CLAUDE.md
git add .claude/settings.json
git add .claude/skills/
git add .claude/agents/
git add .claude/rules/
git add .claude/hooks/
git add .mcp.json
git add .gitignore
git commit -m "Add Claude Code configuration"
git push
```

### What Not to Commit

These are automatically gitignored:
- `CLAUDE.local.md` (personal)
- `.claude/settings.local.json` (personal)
- `.env` (secrets)
- `.claude/agent-memory-local/` (personal memory)

## 🔄 Updating the Template

If you want to pull updates from the original template:

```bash
# Add template as remote
git remote add template /path/to/claude-code-new-project-template

# Pull template updates
git fetch template
git merge template/main --allow-unrelated-histories

# Resolve conflicts (keep your customizations)
```

## 🆘 Troubleshooting

### Memory not loading
```bash
# Check file exists
ls -la CLAUDE.md

# Verify syntax (no special characters at start)
head CLAUDE.md

# Use doctor
/doctor
```

### Hooks not running
```bash
# Make executable
chmod +x .claude/hooks/*.sh

# Test manually
echo '{"tool_input":{"file_path":".env"}}' | ./.claude/hooks/protect-files.sh
```

### Agent not activating
```bash
# Check description is clear
code .claude/agents/my-agent/SKILL.md

# Verify frontmatter
# Must have: name, description
```

### MCP server failing
```bash
# Check status
/mcp

# Re-authenticate
/mcp
# Follow OAuth flow

# Check environment variables
echo $GITHUB_TOKEN
```

## 📚 Resources

- **README.md** - Complete feature guide
- **SETUP.md** - Detailed setup steps
- **STRUCTURE.md** - File structure reference
- **Official Docs** - https://docs.claude.com/claude-code
- **GitHub Issues** - https://github.com/anthropics/claude-code/issues

## 💡 Tips

1. **Keep CLAUDE.md concise** - Only what Claude can't figure out from code
2. **Use skills for workflows** - Repetitive tasks you do often
3. **Use agents for expertise** - Specialized review/debugging/security
4. **Use hooks for automation** - Deterministic tasks (format, validate)
5. **Use rules for standards** - Code style, testing, security conventions
6. **Review permissions regularly** - Add common commands to allow list
7. **Update memory as project evolves** - Keep CLAUDE.md current

---

**Happy coding with Claude!** 🤖✨
