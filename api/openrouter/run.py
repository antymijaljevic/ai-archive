import requests
import json
import time

# | Feature              | Basic Free Tier ($0 Spent) | Verified Free Tier ($10+ Spent) |
# |----------------------|---------------------------|---------------------------------|
# | Daily Request Limit  | 50 requests per day       | 1,000 requests per day          |
# | Requests per Minute  | 20 RPM                    | Variable (Higher)               |
# | Queue Priority       | Lowest (Slowest)          | Normal                          |
# | Cost                 | Completely Free           | Completely Free                 |


# url -s https://openrouter.ai/api/v1/models | \
# jq -r '.data[] | select(.pricing.prompt == "0" and .pricing.completion == "0") | .id'

api_key="suck-it"

openrouter_free_models_ranked = [
    # --- TIER 1: FRONTIER LEVEL (Matches Paid GPT-4o/Claude Sonnet) ---
    "meta-llama/llama-3.1-405b-instruct:free",     # The king of open-weight logic & tool use
    "nousresearch/hermes-3-llama-3.1-405b:free",   # Uncensored, high-steerability version of 405B
    "openai/gpt-oss-120b:free",                    # OpenAI's native open-weights; elite reasoning
    "moonshotai/kimi-k2:free",                     # Specialist in long-context & web-agent tasks
    "meta-llama/llama-3.3-70b-instruct:free",      # Performance of 405B but significantly faster
    "qwen/qwen3-next-80b-a3b-instruct:free",       # 2026 flagship from Alibaba, excels in STEM/Math
    "google/gemini-2.0-flash-exp:free",            # Fast, multimodal, and massive 1M context
    "z-ai/glm-4.5-air:free",                       # Strongest multilingual & agentic model from China

    # --- TIER 2: HIGH-PERFORMANCE MID-RANGE (20B - 40B) ---
    "mistralai/mistral-small-3.1-24b-instruct:free", # The "Goldilocks" model; very reliable
    "google/gemma-3-27b-it:free",                  # Google's best lightweight reasoning model
    "openai/gpt-oss-20b:free",                     # Highly efficient, better than Llama-3-8B
    "nvidia/nemotron-3-nano-30b-a3b:free",         # NVIDIA's optimized MoE for RAG tasks
    "deepseek/deepseek-r1-0528:free",              # Reasoning-focused (Chain-of-Thought) specialist
    "allenai/molmo-2-8b:free",                     # Best-in-class vision-language (multimodal)
    "google/gemma-3-12b-it:free",                  # Solid instruction following for its size
    "upstage/solar-pro-3:free",                    # High throughput, great for summarization

    # --- TIER 3: EFFICIENT / Niche Specialists ---
    "qwen/qwen3-coder:free",                       # Dedicated coding specialist (small version)
    "liquid/lfm-2.5-1.2b-thinking:free",           # First "Thinking" model under 2B parameters
    "tngtech/tng-r1t-chimera:free",                # Merged model optimized for specific tech stacks
    "meta-llama/llama-3.2-3b-instruct:free",       # Best ultra-lightweight mobile/edge model
    "nvidia/nemotron-nano-12b-v2-vl:free",         # Vision-optimized for low-latency tasks
    "arcee-ai/trinity-mini:free",                  # Specialized in domain-specific merging
    "cognitivecomputations/dolphin-mistral-24b-venice-edition:free", # Uncensored/Roleplay
    "qwen/qwen-2.5-vl-7b-instruct:free",           # Older but stable vision model
    "google/gemma-3-4b-it:free",                   # Basic logic for simple chat
    "liquid/lfm-2.5-1.2b-instruct:free",           # Ultra-fast, low-intelligence utility model
    "nvidia/nemotron-nano-9b-v2:free",             # Optimized for NVIDIA hardware inference
]

# model = openrouter_free_models_ranked[3]

models = [
    "moonshotai/kimi-k2.5",
    "google/gemini-3-flash-preview",
    "anthropic/claude-opus-4.5",
    "anthropic/claude-sonnet-4.5",
    "anthropic/claude-haiku-4.5",
    "openai/gpt-5.2",
    "openai/gpt-5.2-codex",
    "x-ai/grok-4"
]

url = "https://openrouter.ai/api/v1/chat/completions"

# Header with the four requested columns
print(f"{'MODEL':<40} | {'TIME':<10} | {'CHARS':<6} | {'RESPONSE'}")
print("-" * 120)

for model in models:
    try:
        start_time = time.perf_counter()
        
        response = requests.post(
            url=url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": model, 
                "messages": [
                    {
                        "role": "user",
                        "content": "Who was the first Croatian president? Answer in one sentence only, please (15-20 words max)."
                    }
                ]
            }),
            timeout=30 
        )
        
        end_time = time.perf_counter()
        latency = end_time - start_time

        if response.status_code == 200:
            content = response.json()['choices'][0]['message']['content'].strip()
            char_count = len(content)
            # Printing full content without truncation
            print(f"{model:<40} | {latency:>8.2f}s | {char_count:<6} | {content}")
        else:
            print(f"{model:<40} | {latency:>8.2f}s | {'N/A':<6} | Error {response.status_code}: {response.text[:30]}")

    except Exception as e:
        print(f"{model:<40} | {'FAILED':>9} | {'N/A':<6} | {str(e)[:50]}")

    time.sleep(0.5)