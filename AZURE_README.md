# Azure OpenAI Integration for Presenton

This repository contains Check Point's fork of [Presenton](https://github.com/presenton/presenton) with Azure OpenAI support.

## 🚀 What's New

This fork adds enterprise-grade Azure OpenAI integration to Presenton:

✅ **Azure OpenAI Native Support** - Works with Azure OpenAI Legacy API endpoints  
✅ **GPT-5 Reasoning Models** - Advanced custom template creation with GPT-5  
✅ **Dual Model Strategy** - Fast gpt-4o-mini for basic, GPT-5 for advanced features  
✅ **Production Ready** - Fully tested with Check Point Azure infrastructure  

## 📋 Quick Start

### Prerequisites

- Docker
- Azure OpenAI endpoint access
- (Optional) Pexels API key for images

### Run with Azure OpenAI

```bash
docker build -t presenton-azure:latest .

docker run -d --name presenton -p 5000:80 \
  -e LLM="custom" \
  -e CUSTOM_LLM_URL="https://your-azure-endpoint.azure-api.net/path" \
  -e CUSTOM_LLM_API_KEY="your-azure-api-key" \
  -e CUSTOM_MODEL="gpt-4o-mini-2024-07-18" \
  -e OPENAI_API_KEY="your-azure-api-key" \
  -e GPT5_MODEL="gpt-5-2025-08-07" \
  -e IMAGE_PROVIDER="pexels" \
  -e PEXELS_API_KEY="your-pexels-key" \
  -e GOOGLE_API_KEY="optional" \
  -v "./app_data:/app_data" \
  presenton-azure:latest
```

Access at: **http://localhost:5000**

## ⚙️ Configuration

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `CUSTOM_LLM_URL` | Azure endpoint URL | `https://your-endpoint.azure-api.net/path` |
| `CUSTOM_LLM_API_KEY` | Azure API key | `your-api-key` |
| `CUSTOM_MODEL` | Fast model for basic presentations | `gpt-4o-mini-2024-07-18` |
| `OPENAI_API_KEY` | Same as `CUSTOM_LLM_API_KEY` (for frontend) | `your-api-key` |

### Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GPT5_MODEL` | Model for custom templates | `gpt-5-2025-08-07` |
| `IMAGE_PROVIDER` | Image service | `pexels` |
| `PEXELS_API_KEY` | Pexels API key | - |
| `GOOGLE_API_KEY` | Google API key | - |

### Model Strategy

- **CUSTOM_MODEL** (gpt-4o-mini): Fast basic presentations (~5-10 seconds)
- **GPT5_MODEL** (gpt-5): Advanced custom templates (~30-60 seconds per slide)

## 🔧 Azure OpenAI Modifications

### Technical Changes

1. **Azure Legacy API Client** (`servers/fastapi/services/llm_client.py`)
   - Auto-detects Azure URLs
   - Uses `AsyncAzureOpenAI` client
   - Handles Azure authentication format

2. **Model Validation Skip** (`servers/fastapi/utils/`)
   - Graceful handling when Azure endpoint lacks `/models` endpoint
   - Proceeds with configured model without validation

3. **GPT-5 Support** (`servers/fastapi/api/v1/ppt/endpoints/slide_to_html.py`)
   - Converted Responses API → Chat Completions API
   - Azure-compatible parameters:
     - `max_completion_tokens` instead of `max_tokens`
     - No `temperature` parameter (GPT-5 default only)
     - 16000 token limit for reasoning
   - Separate GPT5_MODEL configuration

4. **Docker Dependencies** (`Dockerfile`)
   - Added `zstd` for Ollama

## 📚 Usage

### Basic Presentations (Fast)

1. Navigate to http://localhost:5000
2. Enter topic and click "Generate"
3. Uses gpt-4o-mini for speed

### Custom Templates (Advanced)

1. Go to http://localhost:5000/custom-template
2. Upload .pptx file
3. Click "Process File"
4. Uses GPT-5 reasoning for quality
5. Expect 30-60s per slide (reasoning tokens)

### API Documentation

FastAPI docs: http://localhost:5000/docs

## 🔍 Troubleshooting

**Authentication errors (401)**
- Verify `CUSTOM_LLM_API_KEY` is correct
- Check API key has model access

**Slow custom templates**
- Expected: GPT-5 reasoning takes time
- Normal: 30-60 seconds per slide

**Empty GPT-5 responses**
- Fork includes fix: 16000 token limit
- GPT-5 needs tokens for reasoning + content

## 🌳 Branch Structure

- `main` - Sync with upstream Presenton
- `azure-openai-legacy-api` - Azure integration (active)

## 📝 Key Commits

- `fc13b2e` - Initial Azure OpenAI support
- `2d230e7` - GPT-5 Chat Completions API

## 🔗 Links

- **Upstream**: [presenton/presenton](https://github.com/presenton/presenton)
- **Original README**: See [README.md](README.md)
- **Docs**: https://docs.presenton.ai

## 📄 License

Apache License 2.0 (same as upstream)

## 🤝 Support

- Azure OpenAI issues: File in this repo
- Upstream issues: [presenton/presenton](https://github.com/presenton/presenton)

---

**Note**: No sensitive data (API keys, endpoints) are committed to this repository. All configuration is via environment variables.
