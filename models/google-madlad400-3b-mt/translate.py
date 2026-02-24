"""
MADLAD-400 Local Translation Script
Supports: Croatian (hr), Spanish (es), English (en), German (de)

Install dependencies:
    pip install transformers torch sentencepiece accelerate
"""

from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

MODEL_ID = "jbochi/madlad400-3b-mt"

LANGUAGES = {
    "hr": "Croatian",
    "en": "English",
    "es": "Spanish",
    "de": "German",
}

print(f"Loading model: {MODEL_ID}")
print("(First run will download ~11.8GB — use quantized version for faster loading)\n")

tokenizer = T5Tokenizer.from_pretrained(MODEL_ID)
model = T5ForConditionalGeneration.from_pretrained(MODEL_ID, device_map="auto")
model.eval()

print("Model loaded!\n")


def translate(text: str, target_lang: str) -> str:
    if target_lang not in LANGUAGES:
        raise ValueError(f"Unsupported language. Choose from: {list(LANGUAGES.keys())}")

    input_text = f"<2{target_lang}> {text}"
    inputs = tokenizer(input_text, return_tensors="pt").input_ids.to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            input_ids=inputs,
            max_length=512,
            num_beams=4,
            early_stopping=True,
        )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def print_separator():
    print("-" * 50)


# --- Interactive mode ---
print("MADLAD-400 Translation Test")
print("Supported languages:", ", ".join([f"{v} ({k})" for k, v in LANGUAGES.items()]))
print_separator()

# Quick demo
demo_tests = [
    ("Hello, how are you?", "hr"),
    ("Kako si danas?", "en"),
    ("Good morning!", "de"),
    ("Guten Morgen!", "es"),
]

print("Running demo translations...\n")
for text, target in demo_tests:
    result = translate(text, target)
    print(f"  [{target}] {text}")
    print(f"       → {result}")
    print()

print_separator()
print("Interactive mode (type 'quit' to exit)\n")

while True:
    text = input("Text to translate: ").strip()
    if text.lower() in ("quit", "exit", "q"):
        break
    if not text:
        continue

    print(f"Target language ({'/'.join(LANGUAGES.keys())}): ", end="")
    lang = input().strip().lower()
    if lang not in LANGUAGES:
        print(f"Invalid language. Choose from: {list(LANGUAGES.keys())}\n")
        continue

    result = translate(text, lang)
    print(f"→ {result}\n")