# Run Claude Code with Local Ollama Models

This project enables you to run Claude Code CLI with 100% local, private AI models using Ollama's Anthropic API compatibility layer.

## How It Works

The `install-claude-local.sh` script automates the entire setup process:

1. **Detects Your OS** - Automatically identifies macOS or Linux
2. **Installs Ollama** - Downloads and installs Ollama if not already present (via Homebrew on macOS, curl on Linux)
3. **Starts Ollama Service** - Launches the Ollama server in the background
4. **Pulls Your Model** - Downloads your chosen model (defaults to `qwen3-coder-next`)
5. **Installs Claude Code** - Installs the official Claude Code CLI tool
6. **Configures Environment** - Sets up environment variables to redirect Claude Code API calls to your local Ollama instance

### Key Environment Variables

The script configures these variables to point Claude Code to Ollama:
- `ANTHROPIC_BASE_URL="http://localhost:11434"` - Redirects API calls to local Ollama server
- `ANTHROPIC_AUTH_TOKEN="ollama"` - Dummy auth token (Ollama doesn't require authentication)
- `ANTHROPIC_API_KEY="ollama"` - Dummy API key
- `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` - Disables telemetry and cloud features
- `alias lclaude='claude --model $MODEL'` - Convenient alias for running Claude Code with your model

These settings are temporary and only apply to your current terminal session, so they won't affect your normal Claude Code configuration.

## Default Model: Qwen3-Coder 30B

The script defaults to **`qwen3-coder-next`**:

- **Total Parameters**: 30B (30 billion)
- **Active Parameters**: 3.3B (MoE architecture - only 3.3B active at a time)
- **Download Size**: ~19GB
- **Context Length**: 256K tokens (extendable to 1M with YaRN)
- **Hardware Requirements**: 16-24GB VRAM (Q4 quantization)
- **Best For**: Excellent balance of performance and accessibility for most users

### Choosing a Different Model

You can specify any Ollama model when running the script:

```bash
# Use the default 30B model
./install-claude-local.sh

# Use a specific model instead
./install-claude-local.sh qwen2.5-coder:7b       # Smaller, faster model (7B, ~5GB)
./install-claude-local.sh qwen2.5-coder:14b      # Mid-range model (14B, ~9GB)
./install-claude-local.sh orieg/gemma3-tools:27b # Agentic coding assistant (27B, 18GB)
./install-claude-local.sh gpt-oss:120b           # OpenAI's open model (120B, 65GB)
./install-claude-local.sh qwen3-coder:480b       # Largest, best performance (480B, 290GB)
```

## Model Comparison

| Model | Parameters | Download | VRAM | Hardware | Context |
|-------|------------|----------|------|----------|---------|
| [`qwen2.5-coder:7b`](https://ollama.com/library/qwen2.5-coder) | 7B | ~5GB | 6-8GB | RTX 3060, M1 Pro, Budget GPUs | 128K |
| [`qwen2.5-coder:14b`](https://ollama.com/library/qwen2.5-coder) | 14B | ~9GB | 10-12GB | RTX 3080, M2 Pro | 128K |
| [`qwen3-coder-next`](https://ollama.com/library/qwen3-coder) | 30B (3.3B active) | 19GB | 16-24GB | RTX 3090/4090 | 256K |
| [`orieg/gemma3-tools:27b`](https://ollama.com/orieg/gemma3-tools:27b) | 27B | 18GB | 16-24GB | RTX 3090/4090, M2 Max | 128K |
| [`gpt-oss:120b`](https://ollama.com/library/gpt-oss) | 120B (5.1B active) | 65GB | 80-96GB | H100/A100 80GB | 128K |
| [`qwen3-coder:480b`](https://ollama.com/library/qwen3-coder) | 480B (35B active) | 290GB | 250GB+ | Multi-GPU/Mac Studio | 256K |

## Tested on MacBook Pro M2 Max

**Hardware Specs:**
- **Chip:** Apple M2 Max
- **Cores:** 12 (8 performance + 4 efficiency)
- **Memory:** 32GB unified
- **Model:** Mac14,6 (MNWA3CR/A)

This setup uses a **32K context window** by default, which is optimized for the M2 Max's memory constraints while still providing excellent performance for most coding tasks.

| Model | Memory Needed | Status | Notes |
|-------|---------------|--------|-------|
| `qwen2.5-coder:7b` | ~5GB | ✅ Fast | Great for budget hardware |
| `qwen2.5-coder:14b` | ~9GB | ✅ Recommended | Excellent speed/quality balance |
| `qwen3-coder-next` | 19GB | ✅ Recommended | Agentic coding, good context |
| `orieg/gemma3-tools:27b` | 18GB | ✅ Recommended | Agentic coding, good context |
| `gpt-oss:120b`  | 64GB + | ❌ Very Slow  | Agentic coding, good context |
| `qwen3-coder:480b` | 250GB+ | ❌ Not enough | Needs Mac Studio 192GB+ |

## Best Use Cases

- **qwen2.5-coder:7b**: Fastest option for budget hardware. Great for quick coding tasks and low-memory systems.
- **qwen2.5-coder:14b**: Excellent balance of speed and quality. Perfect for most coding tasks on consumer hardware.
- **qwen3-coder-next** (Default): Best balance for consumer hardware. Strong coding with 256K context.
- **orieg/gemma3-tools:27b**: Agentic coding assistant with tool use. Optimized for VS Code integration.
- **gpt-oss:120b**: Production-grade reasoning. Runs on single H100/A100.
- **qwen3-coder:480b**: Best performance for multi-GPU setups or Mac Studio with 256GB+ unified memory.

## LLM Benchmark Comparison

![LLM Benchmark](llm-benchmark.png)