# Project Structure

Complete file structure of the Claude Code template.

```
claude-code-new-project-template/
│
├── README.md                           # Comprehensive guide to Claude Code
├── SETUP.md                            # Step-by-step setup instructions
├── STRUCTURE.md                        # This file - project structure overview
│
├── CLAUDE.md                           # Project memory (team-shared)
├── CLAUDE.local.md                     # Personal overrides (gitignored)
│
├── .env.example                        # Environment variables template
├── .gitignore                          # Git ignore rules (includes Claude Code files)
├── .mcp.json                           # MCP server configuration (team-shared)
│
└── .claude/                            # Claude Code configuration directory
    │
    ├── settings.json                   # Project settings (team-shared)
    ├── settings.local.json             # Personal settings (gitignored)
    ├── CLAUDE.md                       # Alternate memory location
    │
    ├── skills/                         # Custom skills (slash commands)
    │   ├── deploy/
    │   │   └── SKILL.md               # /deploy command
    │   ├── fix-issue/
    │   │   └── SKILL.md               # /fix-issue command
    │   └── review-pr/
    │       └── SKILL.md               # /review-pr command
    │
    ├── agents/                         # Custom subagents
    │   ├── code-reviewer/
    │   │   └── SKILL.md               # Code review specialist
    │   ├── debugger/
    │   │   └── SKILL.md               # Debugging specialist
    │   └── security-checker/
    │       └── SKILL.md               # Security specialist
    │
    ├── rules/                          # Modular rules (auto-loaded)
    │   ├── code-style.md              # General code style
    │   ├── testing.md                 # Testing conventions
    │   ├── security.md                # Security rules
    │   └── api/
    │       └── conventions.md         # API-specific rules (path-scoped)
    │
    ├── hooks/                          # Hook scripts
    │   ├── protect-files.sh           # PreToolUse: Block sensitive files
    │   ├── format-code.sh             # PostToolUse: Auto-format
    │   └── validate-commit.sh         # PreToolUse: Validate commits
    │
    ├── agent-memory/                   # Agent persistent memory (created at runtime)
    └── plugins/                        # Plugin configuration (if using plugins)
```

## File Categories

### 📋 Documentation
- `README.md` - Complete guide with all features
- `SETUP.md` - Setup instructions
- `STRUCTURE.md` - This file

### 💾 Memory Files (Persistent Context)
- `CLAUDE.md` - Project-wide instructions (team)
- `CLAUDE.local.md` - Personal overrides (you only)
- `.claude/CLAUDE.md` - Alternate location

### ⚙️ Configuration
- `.claude/settings.json` - Project settings (team)
- `.claude/settings.local.json` - Personal settings (you only)
- `.mcp.json` - MCP servers (team)
- `.env.example` - Environment variables template

### 🎯 Skills (Slash Commands)
```
/deploy         - Deploy application
/fix-issue      - Fix GitHub issue
/review-pr      - Review pull request
```

### 🤖 Subagents (Specialized AI Assistants)
```
code-reviewer      - Proactive code review
debugger           - Debug errors and failures
security-checker   - Security audit
```

### 📏 Rules (Auto-loaded Instructions)
```
code-style.md         - All files
testing.md            - Test files
security.md           - Security-sensitive code
api/conventions.md    - API routes only (path-scoped)
```

### 🪝 Hooks (Automated Scripts)
```
protect-files.sh      - PreToolUse: Block .env, secrets
format-code.sh        - PostToolUse: Auto-format code
validate-commit.sh    - PreToolUse: Check commit format
```

## File Sharing (Git)

### ✅ Committed (Shared with Team)
```
CLAUDE.md
.claude/settings.json
.claude/skills/
.claude/agents/
.claude/rules/
.claude/hooks/
.mcp.json
.env.example
```

### 🚫 Gitignored (Personal Only)
```
CLAUDE.local.md
.claude/settings.local.json
.claude/agent-memory-local/
.env
```

## Configuration Priority

### Memory Files (Highest to Lowest)
1. Command-line arguments
2. `CLAUDE.local.md` (personal)
3. `.claude/CLAUDE.md` (project)
4. `CLAUDE.md` (project)
5. `~/.claude/CLAUDE.md` (user-wide)

### Settings Files (Highest to Lowest)
1. Managed (system admin)
2. CLI arguments
3. `.claude/settings.local.json` (personal)
4. `.claude/settings.json` (project)
5. `~/.claude/settings.json` (user-wide)

## Runtime Files (Created Automatically)

These files are created by Claude Code during use:

```
.claude/
├── agent-memory/              # Project agent memory
│   └── <agent-name>/
│       └── MEMORY.md
├── agent-memory-local/        # Personal agent memory
├── plans/                     # Plan mode plans
├── transcripts/               # Session transcripts
└── cache/                     # Cache files
```

## Adding New Files

### Add a Skill
```bash
mkdir .claude/skills/my-skill
cat > .claude/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: What this skill does
---

# Instructions here
EOF
```

### Add a Subagent
```bash
mkdir .claude/agents/my-agent
cat > .claude/agents/my-agent/SKILL.md << 'EOF'
---
name: my-agent
description: What this agent does
tools: Read, Grep, Glob
---

# Agent instructions here
EOF
```

### Add a Rule
```bash
cat > .claude/rules/my-rule.md << 'EOF'
# My Custom Rule

Rules apply to all files by default.

Use frontmatter to scope to specific paths:
---
paths:
  - "src/**/*.ts"
---
EOF
```

### Add a Hook
```bash
cat > .claude/hooks/my-hook.sh << 'EOF'
#!/bin/bash
# Hook logic here
exit 0
EOF

chmod +x .claude/hooks/my-hook.sh
```

## Size Limits

- **CLAUDE.md**: Keep under ~2000 lines (only first portion loaded)
- **MEMORY.md**: First 200 lines loaded at startup
- **Rules**: All rules loaded (keep focused)
- **Skills**: Loaded on-demand (no hard limit)
- **Agents**: Loaded on-demand (no hard limit)

## Best Practices

1. **Memory Files**: Concise, focused, no redundancy
2. **Skills**: Clear purpose, good examples
3. **Agents**: Specific expertise, appropriate tools
4. **Rules**: Organized by topic, path-scoped when possible
5. **Hooks**: Reliable, fast, clear error messages

---

**Tip**: Use `/doctor` to check for configuration issues
