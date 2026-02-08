# Tmux + Claude Agent Team – Quick Setup

## Install tmux

```bash
brew update && brew install tmux
```

## Auto-start tmux with terminal (Optional, skip this)
if [[ -z "$TMUX" && -n "$PS1" ]]; then
    tmux attach-session -t default 2>/dev/null || tmux new-session -s default
fi

## Tmux config (~/.tmux.conf)

```bash
set-hook -g after-split-window 'select-layout even-horizontal'
set-hook -g after-kill-pane 'select-layout even-horizontal'
set -g pane-active-border-style "fg=#8B0000"
set -g pane-border-style "fg=#444444"
```

Reload:

```bash
tmux source-file ~/.tmux.conf
```

## Claude Code config (~/.claude/settings.json)

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "teammateMode": "tmux"
}
```

## Run

```bash
tmux
claude
```

## Claude prompt (agent team)

```text
Create an agent team to test solution B for Q4.

Spawn 3 teammates:
QA Exam Engineer
Linux Senior Engineer
Kubernetes Senior Engineer
```

## Tmux basics

* `Ctrl + b , x` → new window
* `Ctrl + b , [0-9]` → switch window
* `Ctrl + b , %` → vertical split
* `Ctrl + b , "` → horizontal split
* `Ctrl + b , ← →` → switch panes
* `Ctrl + b , x` → close pane/window