# Claude Code Project Template

A comprehensive template for Claude Code projects with all configuration files, examples, and best practices.

## Quick Start

1. Copy this template to your new project directory
2. Customize `CLAUDE.md` with your project-specific instructions
3. Update `.claude/settings.json` with your project settings
4. Add MCP servers to `.mcp.json` if needed
5. Customize skills, agents, and hooks as needed

## Table of Contents

- [File Structure](#file-structure)
- [Memory Files (CLAUDE.md)](#memory-files-claudemd)
- [Settings Configuration](#settings-configuration)
- [Skills](#skills)
- [Hooks](#hooks)
- [Subagents](#subagents)
- [MCP Servers](#mcp-servers)
- [Modular Rules](#modular-rules)
- [Best Practices](#best-practices)
- [Quick Reference](#quick-reference)

---

## File Structure

```
your-project/
├── README.md                           # This file
├── CLAUDE.md                           # Project memory (team-shared)
├── CLAUDE.local.md                     # Personal overrides (gitignored)
├── .mcp.json                           # MCP servers (team-shared)
├── .gitignore                          # Ignore local files
│
└── .claude/                            # Claude Code configuration
    ├── settings.json                   # Project settings (team-shared)
    ├── settings.local.json             # Personal settings (gitignored)
    ├── CLAUDE.md                       # Alternate memory location
    │
    ├── skills/                         # Custom skills (slash commands)
    │   ├── deploy/
    │   │   ├── SKILL.md               # Main skill instructions
    │   │   └── checklist.md           # Supporting files
    │   ├── fix-issue/SKILL.md
    │   └── review-pr/SKILL.md
    │
    ├── agents/                         # Custom subagents
    │   ├── code-reviewer/SKILL.md
    │   ├── debugger/SKILL.md
    │   └── security-checker/SKILL.md
    │
    ├── rules/                          # Modular rules (auto-loaded)
    │   ├── code-style.md
    │   ├── testing.md
    │   ├── security.md
    │   └── api/                        # Subdirectories supported
    │       └── conventions.md
    │
    ├── hooks/                          # Hook scripts
    │   ├── protect-files.sh
    │   ├── validate-commit.sh
    │   └── format-code.sh
    │
    ├── agent-memory/                   # Agent persistent memory (project)
    │   └── <agent-name>/MEMORY.md
    │
    └── plugins/                        # Plugin configuration
```

---

## Memory Files (CLAUDE.md)

### Priority System (Highest to Lowest)

1. **System-level managed policy** (organization-wide)
2. **Command-line arguments** (session-specific)
3. **`./CLAUDE.local.md`** (personal project overrides, gitignored)
4. **`./.claude/CLAUDE.md`** (project-wide, team-shared)
5. **`./CLAUDE.md`** (project-wide, team-shared)
6. **`~/.claude/CLAUDE.md`** (personal, all your projects)
7. **System-level organization policy** (lowest priority)

### What to Include in CLAUDE.md

✅ **Include:**
- Commands Claude can't guess (`npm run dev:staging`)
- Project-specific conventions (branch naming, PR format)
- Testing instructions (`npm run test:watch`)
- Architecture decisions (why we use X instead of Y)
- Required environment variables
- Build/deployment commands
- Non-obvious behaviors or gotchas

❌ **Exclude:**
- Standard conventions Claude already knows
- Information easily found in code
- Detailed API docs (link instead)
- Frequently changing information
- Self-evident practices

### Example Structure

```markdown
# Project: My Awesome App

## Commands
- Build: `npm run build`
- Test: `npm run test` (requires Docker)
- Deploy: `npm run deploy:staging`

## Code Style
- Use functional components with hooks
- Prefer async/await over promises
- All API calls in `src/api/` directory

## Git Workflow
- Branch naming: `feature/description` or `fix/description`
- Always create PR for review
- Run tests before pushing

## Architecture
- Using Zustand for state (not Redux - lighter weight)
- API layer uses React Query for caching
- Tests use Vitest (not Jest - faster)

## Environment
Required: `DATABASE_URL`, `API_KEY`
Optional: `DEBUG=true` for verbose logging
```

---

## Settings Configuration

### Priority (Highest to Lowest)

1. **Managed** (system admin deployments)
2. **CLI arguments** (`--allowedTools`)
3. **`.claude/settings.local.json`** (personal, gitignored)
4. **`.claude/settings.json`** (team-shared)
5. **`~/.claude/settings.json`** (user-wide)

### Common Settings

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",

  "model": "claude-sonnet-4-5-20250929",

  "permissions": {
    "allow": [
      "Bash(npm run test)",
      "Bash(npm run lint)"
    ],
    "deny": [
      "Read(.env*)",
      "Read(**/*secret*)",
      "Bash(rm -rf *)"
    ],
    "ask": [
      "Bash(git push *)",
      "Bash(npm run deploy*)"
    ],
    "defaultMode": "acceptEdits"
  },

  "env": {
    "NODE_ENV": "development"
  },

  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "npx prettier --write $FILE"
        }]
      }
    ]
  },

  "attribution": {
    "commit": "🤖 Generated with Claude Code",
    "pr": "🤖 Generated with Claude Code"
  }
}
```

---

## Skills

### What are Skills?

Skills are reusable workflows that become **slash commands** like `/deploy`, `/review-pr`, `/fix-issue`.

### Skill Structure

```
.claude/skills/my-skill/
├── SKILL.md              # Main instructions (required)
├── checklist.md          # Supporting files
└── examples/
    └── good-example.md
```

### Frontmatter Fields

```yaml
---
name: fix-issue                           # Becomes /fix-issue
description: Fix GitHub issue             # When to use
disable-model-invocation: true            # Only user can invoke
argument-hint: [issue-number]             # Help text
allowed-tools: Read, Grep, Bash           # Auto-approved tools
model: sonnet                             # Override model
context: fork                             # Run in subagent
---
```

### Example Skill: /deploy

```markdown
---
name: deploy
description: Deploy application to production
disable-model-invocation: true
argument-hint: [environment]
---

Deploy to $ARGUMENTS environment:

1. Verify all tests pass: `npm run test`
2. Build production bundle: `npm run build`
3. Run deployment: `npm run deploy:$ARGUMENTS`
4. Verify deployment health check
5. Create deployment tag in git

⚠️ ASK USER FOR CONFIRMATION before deploying to production!
```

### String Substitutions

- `$ARGUMENTS` - All arguments
- `$ARGUMENTS[0]` or `$0` - First argument
- `$ARGUMENTS[1]` or `$1` - Second argument
- `!`command`` - Execute and inject output

---

## Hooks

### What are Hooks?

Hooks are **shell scripts** that run automatically at specific events. Unlike skills (LLM-driven), hooks are **deterministic automation**.

### Hook Events

| Event | When It Fires | Common Use |
|-------|---------------|-----------|
| `SessionStart` | Session begins | Inject context |
| `UserPromptSubmit` | You submit prompt | Validate input |
| `PreToolUse` | Before tool runs | Block dangerous commands |
| `PostToolUse` | After tool succeeds | Auto-format, lint |
| `PermissionRequest` | Permission dialog | Auto-approve safe commands |
| `Stop` | Claude finishes | Verify tasks complete |

### Configuration

**Interactive:** `/hooks`

**Manual:** Edit `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "./.claude/hooks/format-code.sh"
        }]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "./.claude/hooks/validate-command.sh"
        }]
      }
    ]
  }
}
```

### Hook Exit Codes

- **0** - Allow action
- **2** - Block action (write reason to stderr)
- **Other** - Allow but log stderr

---

## Subagents

### What are Subagents?

Specialized AI assistants with **isolated context windows**, their own tools, and permissions.

### Built-in Subagents

- **Explore** (Haiku, read-only) - Fast codebase search
- **Plan** (inherits, read-only) - Planning mode
- **General-purpose** (inherits, all tools) - Complex tasks
- **Bash** (inherits, bash only) - Terminal operations

### Creating Custom Subagents

**Interactive:** `/agents`

**Manual:** Create `.claude/agents/my-agent/SKILL.md`:

```markdown
---
name: code-reviewer
description: Expert code reviewer. Use proactively after code changes.
tools: Read, Grep, Glob, Bash
model: sonnet
permissionMode: default
memory: project
---

You are a senior code reviewer ensuring quality and security.

Review checklist:
- Code clarity and readability
- Security vulnerabilities
- Performance issues
- Test coverage
- Error handling

Provide feedback organized by priority:
1. Critical (must fix)
2. Warnings (should fix)
3. Suggestions (consider)
```

### Subagent Scopes

| Location | Scope | Priority |
|----------|-------|----------|
| `--agents` CLI flag | Session | 1 (highest) |
| `.claude/agents/` | Project | 2 |
| `~/.claude/agents/` | User | 3 |
| Plugin `agents/` | Plugin | 4 (lowest) |

---

## MCP Servers

### What is MCP?

**Model Context Protocol** - Connects Claude to external services (databases, APIs, tools).

### Installation

```bash
# Remote HTTP (recommended)
claude mcp add --transport http github https://mcp.github.com

# Local stdio
claude mcp add --transport stdio --env API_KEY=xxx my-server \
  -- npx -y my-mcp-server

# Scopes
--scope local      # Just you (default)
--scope project    # Team via .mcp.json
--scope user       # You across all projects
```

### Management

```bash
claude mcp list              # List all
claude mcp get github        # Details
claude mcp remove github     # Remove
/mcp                         # Check status in session
```

### Using MCP Resources

```bash
> Analyze @github:issue://123
> Review @docs:file://api/spec
> Query @postgres:table://users
```

### .mcp.json Structure (Project Scope)

```json
{
  "mcpServers": {
    "github": {
      "transport": "http",
      "url": "https://mcp.github.com",
      "headers": {
        "Authorization": "Bearer ${GITHUB_TOKEN}"
      }
    },
    "postgres": {
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "postgres-mcp-server"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

---

## Modular Rules

### What are Modular Rules?

Auto-loaded markdown files in `.claude/rules/` that provide organized instructions.

### Path-Specific Rules

Use YAML frontmatter to apply rules only to specific files:

```markdown
---
paths:
  - "src/api/**/*.ts"
  - "lib/api/**/*.ts"
---

# API Conventions

All API endpoints must:
- Return consistent error format
- Include request validation
- Use proper HTTP status codes
- Log all errors
```

### Organization

```
.claude/rules/
├── code-style.md           # General code style
├── testing.md              # Testing conventions
├── security.md             # Security rules
├── api/
│   ├── conventions.md      # API-specific rules
│   └── error-handling.md
└── frontend/
    ├── components.md
    └── state-management.md
```

---

## Best Practices

### 1. Memory Files (CLAUDE.md)

- ✅ Keep concise and focused
- ✅ Update when conventions change
- ✅ Use CLAUDE.local.md for personal preferences
- ❌ Don't duplicate what's in code
- ❌ Don't include frequently changing info

### 2. Skills

- ✅ Use for repeatable workflows
- ✅ Set `disable-model-invocation: true` for risky operations (deploy, push)
- ✅ Include supporting files in skill directory
- ❌ Don't create skills for one-off tasks

### 3. Hooks

- ✅ Use for deterministic automation (format, lint, validate)
- ✅ Make scripts executable: `chmod +x .claude/hooks/*.sh`
- ✅ Test hooks independently before adding
- ❌ Don't use hooks for decisions requiring judgment (use skills)

### 4. Subagents

- ✅ Create for specialized repeated tasks
- ✅ Use `memory: project` for cross-session learning
- ✅ Restrict tools appropriately (`tools: Read, Grep`)
- ❌ Don't create too many (3-5 is usually enough)

### 5. Settings

- ✅ Use `.claude/settings.json` for team settings
- ✅ Use `.claude/settings.local.json` for personal settings
- ✅ Use `deny` patterns to protect sensitive files
- ❌ Don't commit settings.local.json or CLAUDE.local.md

### 6. Git

Always add to `.gitignore`:
```gitignore
# Claude Code - Personal files
CLAUDE.local.md
.claude/settings.local.json
.claude/agent-memory-local/

# Claude Code - Temporary files
.claude/plans/
```

---

## Quick Reference

### Commands

```bash
# Session Management
/clear              # Clear context
/compact            # Manual compaction
/rename             # Rename session
claude --continue   # Resume last session
claude --resume     # Choose session

# Configuration
/config             # Interactive settings
/hooks              # Manage hooks
/agents             # Manage subagents
/mcp                # Check MCP servers
/keybindings        # Edit keybindings
/statusline         # Configure status

# Utilities
/debug              # View debug log
/doctor             # Check for issues
/insights           # Session analysis
/help               # Get help

# Modes
/plan               # Enter plan mode
/normal             # Normal mode
/sandbox            # Sandbox mode
```

### Environment Variables

```bash
# MCP
MCP_TIMEOUT=10000
MAX_MCP_OUTPUT_TOKENS=50000
ENABLE_TOOL_SEARCH=auto:5

# Behavior
CLAUDE_CODE_ENABLE_TELEMETRY=1
CLAUDE_CODE_DISABLE_AUTO_MEMORY=0
CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=80

# Model
ANTHROPIC_API_KEY=sk-...
ANTHROPIC_MODEL=claude-opus-4-6
```

### Keyboard Shortcuts (Default)

```
Ctrl+C          Interrupt
Ctrl+D          Exit
Enter           Submit
Escape          Cancel
Ctrl+T          Toggle todos
Ctrl+O          Toggle transcript
Ctrl+R          History search
Cmd+P           Model picker
Esc+Esc         Rewind
```

### Permission Modes

```json
"defaultMode": "acceptEdits"      // Auto-approve edits
"defaultMode": "dontAsk"          // Auto-deny prompts
"defaultMode": "bypassPermissions" // Skip all checks ⚠️
"defaultMode": "plan"             // Read-only
```

---

## File Scope Summary

| File | Scope | Shared via Git | Purpose |
|------|-------|----------------|---------|
| `CLAUDE.md` | Project | ✅ Yes | Team conventions |
| `CLAUDE.local.md` | Personal | ❌ No | Your preferences |
| `.claude/settings.json` | Project | ✅ Yes | Team settings |
| `.claude/settings.local.json` | Personal | ❌ No | Your settings |
| `.mcp.json` | Project | ✅ Yes | Team MCP servers |
| `.claude/skills/` | Project | ✅ Yes | Team workflows |
| `.claude/agents/` | Project | ✅ Yes | Team subagents |
| `.claude/rules/` | Project | ✅ Yes | Team rules |
| `.claude/hooks/` | Project | ✅ Yes | Hook scripts |

---

## Resources

- **Official Docs**: https://docs.claude.com/claude-code
- **GitHub Issues**: https://github.com/anthropics/claude-code/issues
- **MCP Servers**: https://github.com/modelcontextprotocol/servers
- **Help Command**: `/help` in any session

---

## Getting Started Checklist

- [ ] Copy template to your project
- [ ] Update `CLAUDE.md` with project info
- [ ] Configure `.claude/settings.json` permissions
- [ ] Add MCP servers to `.mcp.json` if needed
- [ ] Create custom skills for common workflows
- [ ] Set up hooks for auto-formatting
- [ ] Create specialized subagents if needed
- [ ] Add to `.gitignore`: `CLAUDE.local.md`, `.claude/settings.local.json`
- [ ] Test configuration with `/doctor`
- [ ] Share with team via git

---

**Template Version:** 1.0
**Last Updated:** 2026-02-16
**Claude Code Compatibility:** Latest

Happy coding with Claude! 🤖
