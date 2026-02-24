# MADLAD-400 Local Translation

Local machine translation using Google's [MADLAD-400-3B-MT](https://huggingface.co/google/madlad400-3b-mt) model.

MT (Machine Translation)
Purpose-built for one task: translate text from language A → B. That's it.

LLM (Large Language Model)
General purpose: write, reason, code, summarize, translate, chat — anything.

**License:** Apache 2.0 — commercial use allowed ✅

---

## Supported Languages

| Code | Language |
|------|----------|
| `hr` | Croatian |
| `en` | English  |
| `es` | Spanish  |
| `de` | German   |

---

## Requirements

- Python 3.8+
- ~12GB disk space (model download on first run)
- ~16GB RAM (CPU) or 6GB VRAM (GPU)

---

## Installation

```bash
pip3 install -r requirements.txt
```

---

## Usage

```bash
python3 translate.py
```

On first run the model (~11.8GB) will be downloaded automatically from HuggingFace and cached locally. Subsequent runs load from cache instantly.

### Demo output

When started, the script runs a few built-in demo translations:

```
[hr] Hello, how are you?
     → Kako si?

[en] Kako si danas?
     → How are you today?

[de] Good morning!
     → Guten Morgen!

[es] Guten Morgen!
     → Buenos días!
```

### Interactive mode

After the demo, you'll be prompted to enter your own text:

```
Text to translate: Gdje je najbliži restoran?
Target language (hr/en/es/de): en
→ Where is the nearest restaurant?
```

Type `quit` to exit.

---

## Tips

- Prefix is handled automatically — you don't need to type `<2hr>` yourself
- Longer sentences may be slower on CPU; GPU is recommended for production use
- For a much lighter setup (~1.65GB), use the quantized GGUF version via llama.cpp:

```bash
cargo run --example quantized-t5 --release -- \
  --model-id "jbochi/madlad400-3b-mt" \
  --weight-file "model-q4k.gguf" \
  --prompt "<2hr> Hello!"
```

---

## Files

```
.
├── translate.py       # Main script
├── requirements.txt   # Python dependencies
└── README.md          # This file
```