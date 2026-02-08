#!/usr/bin/env bash
set -e

clear

# ============================================================================
# SETTINGS
# ============================================================================

# 256K Context = 262144
# 64K Context = 65536
# 32K Context = 32768
# 25K Context = 25600
MODEL="${1:-qwen3-coder:latest}"
CONTEXT_WINDOW='25600'
K_WINDOW=$(( CONTEXT_WINDOW / 1024 ))
CUSTOM_MODEL_NAME="${MODEL//:/-}-${K_WINDOW}k"

echo "🚀 Setting up Claude Code with $MODEL ($K_WINDOW Context Window)"
echo "--------------------------------------------------------"

# --- OS DETECTION ---
OS="$(uname -s)"

# --- INSTALL OLLAMA ---
if ! command -v ollama &>/dev/null; then
  echo "📦 Ollama not found. Installing..."
  if [[ "$OS" == "Darwin" ]]; then
    brew install ollama
  elif [[ "$OS" == "Linux" ]]; then
    curl -fsSL https://ollama.com/install.sh | sh
  fi
else
  echo "✅ Ollama $(ollama --version) already installed"
fi

# --- KILL EXISTING OLLAMA PROCESSES ---
if pgrep -x "ollama" > /dev/null; then
    echo "🛑 Stopping existing Ollama processes..."
    pkill -TERM ollama 2>/dev/null || true
    sleep 2
    # Force kill if still running
    if pgrep -x "ollama" > /dev/null; then
        echo "⚠️  Force killing remaining Ollama processes..."
        pkill -KILL ollama 2>/dev/null || true
        sleep 1
    fi
    echo "✅ Ollama processes stopped"
fi

# --- START OLLAMA ---
echo "▶️  Starting Ollama..."
ollama serve >/dev/null 2>&1 &
sleep 5

# --- PULL & CONFIGURE MODEL ---
echo "🧠 Ensuring base model $MODEL is present..."
ollama pull "$MODEL"

echo "🛠️  Creating custom model $CUSTOM_MODEL_NAME with $K_WINDOW context window..."

cat <<EOF > .temp_modelfile
FROM $MODEL
PARAMETER num_ctx $CONTEXT_WINDOW
EOF

if ollama create "$CUSTOM_MODEL_NAME" -f .temp_modelfile; then
    echo "✅ Model $CUSTOM_MODEL_NAME created successfully."
    rm .temp_modelfile
else
    echo "❌ Error: Failed to create custom model."
    rm .temp_modelfile
    exit 1
fi

# --- INSTALL CLAUDE CODE ---
if ! command -v claude &>/dev/null; then
  echo "🤖 Installing Claude Code..."
  curl -fsSL https://claude.ai/install.sh | bash
else
  echo "✅ Claude Code already installed"
fi

# --- FINAL MESSAGE ---
echo ""
echo "🎉 READY!"
echo "--------------------------------------------------------"
echo "🔍 Verification: While running lclaude, open another terminal and run:"
echo "   ollama ps"
echo "   It should show CONTEXT: $CONTEXT_WINDOW"
echo ""
echo "📋 Copy and paste this block into your terminal:"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cat <<EOF
export ANTHROPIC_BASE_URL="http://localhost:11434"
export ANTHROPIC_AUTH_TOKEN="ollama"
export ANTHROPIC_API_KEY="ollama"
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
alias lclaude='claude --model $CUSTOM_MODEL_NAME'

# Now run: lclaude
EOF
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"