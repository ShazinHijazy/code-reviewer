# Open-Source LLM Integration Guide

## Overview

The Code Reviewer has been migrated to use **only open-source LLMs** that run locally via **Ollama**. No API keys required!

## What Changed

### ❌ Removed (Paid APIs)
- Claude (Anthropic) - Removed
- OpenAI GPT-4 - Removed  
- Google Gemini - Removed

### ✅ Added (Open-Source Local)
- **Ollama** - Local inference engine
- **Mistral 7B** - Fast, great for code (recommended)
- **CodeLLaMA** - Specialized for code
- **LLaMA 2** - Most capable (needs GPU)
- **Dolphin** - Fine-tuned variant
- **Orca Mini** - Lightweight (3B)

## Installation & Setup

### 1. Install Ollama

**macOS:**
```bash
brew install ollama
# or download from: https://ollama.ai/download
```

**Linux:**
```bash
curl https://ollama.ai/install.sh | sh
```

**Windows:**
- Download from: https://ollama.ai/download/OllamaSetup.exe

### 2. Start Ollama Service

In a new terminal:
```bash
ollama serve
```

This starts the Ollama service on `http://localhost:11434`

### 3. Pull a Model

In another terminal:
```bash
# Recommended - fast and good quality
ollama pull mistral

# Best for code - specialized model
ollama pull codellama

# Most capable - needs GPU
ollama pull llama2

# Lightweight - good for testing
ollama pull orca-mini
```

### 4. Verify Installation

```bash
# List installed models
ollama list

# Test a model
ollama run mistral "Write a Python function to add two numbers"
```

### 5. Code Reviewer Auto-Detection

Once Ollama is running with a model installed, the Code Reviewer will automatically:
- Detect Ollama running on localhost:11434
- Use the latest installed model
- Show "✓ Open-Source LLM Handler initialized" on startup

## Usage

### Via Web UI

1. Open http://127.0.0.1:5000
2. Go to "LLM Refine" tab
3. Your code will be refined using the local model
4. Status shows which model is active

### Via API

**Refine Code:**
```bash
curl -X POST http://127.0.0.1:5000/api/refine-code \
  -H "Content-Type: application/json" \
  -d '{
    "code": "for i in range(len(items)): result = result + items[i]",
    "language": "python",
    "issues": []
  }'
```

**Check Provider Status:**
```bash
curl http://127.0.0.1:5000/api/llm-providers
```

## Model Recommendations

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| **Mistral** | 7B | ⚡⚡⚡ | ⭐⭐⭐⭐ | General code review (Recommended) |
| **CodeLLaMA** | 7B-34B | ⚡⚡ | ⭐⭐⭐⭐⭐ | Code-specific tasks |
| **LLaMA 2** | 7B-70B | ⚡ | ⭐⭐⭐⭐⭐ | High quality (needs GPU) |
| **Orca Mini** | 3B | ⚡⚡⚡ | ⭐⭐⭐ | Testing/lightweight |
| **Dolphin** | 7B-70B | ⚡⚡ | ⭐⭐⭐⭐⭐ | Best instruction following |

## Performance Tips

### System Requirements
- **CPU only**: 8GB RAM minimum, 4GB RAM with swap
- **GPU**: NVIDIA (CUDA), AMD (ROCm), or Apple Silicon (Metal) - 4GB VRAM minimum
- **Storage**: 5GB per model (Mistral 7B ≈ 4GB)

### GPU Acceleration

**NVIDIA (CUDA):**
```bash
# On macOS with CUDA - already optimized
# On Linux/Windows - install NVIDIA CUDA Toolkit
# Ollama auto-detects NVIDIA GPUs
```

**Apple Silicon (Metal):**
```bash
# Automatic - Ollama uses Metal by default on Apple Silicon
# Models run significantly faster
```

**AMD (ROCm):**
```bash
# Install AMD ROCm toolkit
# Set environment: export OLLAMA_CUDA_DRIVER=rocm
```

### Memory Management

**Reduce Memory Usage:**
```bash
# Use smaller models
ollama pull orca-mini

# Or quantized versions
ollama pull mistral:7b-q2_K  # 2-bit quantization - faster, lower quality
ollama pull mistral:7b-q4_K  # 4-bit quantization - good balance
```

**Faster Responses:**
1. Use GPU if available
2. Start with Mistral (7B)
3. Use quantized models for lower-end hardware

## Fallback Behavior

If Ollama is not running:
- Code Reviewer automatically uses **demo mode**
- Demo mode uses pattern-based refinements (no LLM required)
- System remains fully functional
- Enhancements and static analysis still work

## Architecture

```
Code Reviewer
├── Static Analysis (30+ languages)
│   ├── AST parsing (Python)
│   └── Regex patterns (multi-language)
│
└── LLM Refinement (Open-Source)
    ├── Ollama Handler (localhost:11434)
    │   ├── Mistral
    │   ├── CodeLLaMA
    │   └── LLaMA 2
    │
    └── Demo Fallback (Pattern-based)
        └── Works without Ollama
```

## File Structure

```
code-reviewer/
├── opensource_llm.py      # Open-source LLM integration
├── llm_handler.py         # Replaced with open-source version
├── app.py                 # Flask API (updated)
├── code_reviewer.py       # Static analysis
├── enhancements.py        # Enhancement suggestions
└── templates/index.html   # Web UI
```

## Benefits

✅ **No API Keys** - Everything runs locally  
✅ **No Subscription** - Free open-source models  
✅ **No Network Required** - After initial model download  
✅ **Complete Privacy** - Code never leaves your machine  
✅ **Full Control** - Run locally, customize as needed  
✅ **Cost Effective** - One-time download, unlimited usage  

## Troubleshooting

### Ollama not connecting
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it:
ollama serve

# Check which models are installed:
ollama list
```

### Slow responses
```bash
# Using CPU-only - install GPU drivers
# Check GPU usage in Ollama output:
ollama run mistral  # Shows GPU/CPU usage

# Try a smaller model:
ollama pull orca-mini
```

### Out of memory
```bash
# Use quantized model (smaller)
ollama pull mistral:7b-q4_K

# Or use smaller model
ollama pull orca-mini
```

### Model not found
```bash
# Pull the model first
ollama pull mistral

# Verify it's installed
ollama list
```

## Next Steps

1. **Install Ollama**: https://ollama.ai/download
2. **Pull a model**: `ollama pull mistral`
3. **Start Ollama**: `ollama serve`
4. **Restart Code Reviewer**: Server auto-detects Ollama
5. **Try LLM Refine**: Go to web UI and use the feature

## Support & Resources

- **Ollama Docs**: https://github.com/ollama/ollama
- **Available Models**: https://ollama.ai/library
- **GitHub Issues**: Report bugs or feature requests
- **Model Sizes**: https://ollama.ai/library

---

**Key Point**: All models run 100% locally. No data leaves your machine. No API keys needed. Completely free and open-source.
