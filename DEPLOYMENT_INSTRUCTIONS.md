# Presenton Azure OpenAI - Deployment Instructions

## Quick Start

This is a ready-to-use Docker image of Presenton (open-source AI presentation generator) configured to work with Check Point's Azure OpenAI infrastructure.

### Pull and Run (Single Command)

```bash
docker pull othmank/presenton-azure:latest && \
docker run -d --name presenton -p 5000:80 \
  -e LLM="custom" \
  -e CUSTOM_LLM_URL="https://staging-openai.azure-api.net/openai-gw-proxy-dev" \
  -e CUSTOM_LLM_API_KEY="YOUR_AZURE_API_KEY" \
  -e CUSTOM_MODEL="gpt-4o-mini-2024-07-18" \
  -e OPENAI_API_KEY="YOUR_AZURE_API_KEY" \
  -e GOOGLE_API_KEY="dummy-key-not-needed" \
  -e IMAGE_PROVIDER="pexels" \
  -e PEXELS_API_KEY="YOUR_PEXELS_API_KEY" \
  -e GPT5_MODEL="gpt-5-2025-08-07" \
  -e CAN_CHANGE_KEYS="false" \
  -v "./app_data:/app_data" \
  othmank/presenton-azure:latest
```

**Note:** Replace `YOUR_AZURE_API_KEY` and `YOUR_PEXELS_API_KEY` with your actual API keys.

### Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

## What This Image Provides

### Features
- ✅ **Basic Presentations**: Fast generation using GPT-4o-mini (optimized for speed)
- ✅ **Custom Templates**: Advanced HTML/CSS/JS template creation using GPT-5 (with reasoning)
- ✅ **Image Generation**: Integrated with Pexels API for presentation images
- ✅ **Azure OpenAI Native Support**: Full compatibility with Check Point's Azure infrastructure
- ✅ **Multi-format Export**: PPT, PDF, HTML export capabilities

### Architecture
- **Frontend**: Next.js 14.2.31 (TypeScript/React)
- **Backend**: Python 3.11 FastAPI
- **Database**: SQLite
- **Vector Store**: ChromaDB with Ollama embeddings
- **Size**: 15.9GB uncompressed, 4.87GB compressed

## Environment Variables Reference

### Required Variables

| Variable | Purpose | Example Value |
|----------|---------|---------------|
| `LLM` | LLM provider selection | `custom` (for Azure OpenAI) |
| `CUSTOM_LLM_URL` | Azure OpenAI endpoint | `https://staging-openai.azure-api.net/openai-gw-proxy-dev` |
| `CUSTOM_LLM_API_KEY` | Azure OpenAI API key | Your Azure API key |
| `CUSTOM_MODEL` | Primary model for basic presentations | `gpt-4o-mini-2024-07-18` |
| `GPT5_MODEL` | Advanced model for custom templates | `gpt-5-2025-08-07` |
| `IMAGE_PROVIDER` | Image service provider | `pexels` |
| `PEXELS_API_KEY` | Pexels API key | Your Pexels API key |

### Optional Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `CAN_CHANGE_KEYS` | Allow users to modify API keys in UI | `false` (recommended) |
| `OPENAI_API_KEY` | Fallback key for certain features | Same as `CUSTOM_LLM_API_KEY` |
| `GOOGLE_API_KEY` | Google services (not used) | `dummy-key-not-needed` |

## Performance Notes

### Dual-Model Strategy

This deployment uses two models for optimal performance:

1. **GPT-4o-mini** (`CUSTOM_MODEL`):
   - Used for: Basic presentations, quick generation
   - Speed: Fast (~10-30 seconds per presentation)
   - Quota: 10k tokens/day, 500 requests/min

2. **GPT-5** (`GPT5_MODEL`):
   - Used for: Custom template creation, HTML editing
   - Speed: Slower (60-120 seconds due to reasoning)
   - Quota: Lower limits, use sparingly

### Expected Performance
- Basic presentation (5 slides): 15-30 seconds
- Custom template creation: 60-120 seconds (includes reasoning phase)
- Image insertion: 2-5 seconds per image (Pexels API)

## Troubleshooting

### Container Won't Start

**Check port availability:**
```bash
lsof -i :5000
# Kill any process using port 5000 or use a different port
docker run -d --name presenton -p 8080:80 ... othmank/presenton-azure:latest
```

**Check logs:**
```bash
docker logs presenton
```

### Authentication Errors (401)

**Problem**: "Invalid API key" or "Unauthorized"

**Solution**:
- Verify your Azure API key is correct
- Ensure the key has access to the specified models
- Check that the endpoint URL is correct

### Empty Presentations

**Problem**: Presentations generate but slides are empty

**Solution**:
- Check Azure OpenAI quota (may be rate-limited)
- Verify model names match your Azure deployment
- Check logs: `docker logs presenton`

### Slow Custom Template Creation

**Expected behavior**: GPT-5 uses reasoning tokens, takes 60-120 seconds. This is normal.

If it takes longer than 2 minutes:
- Check Azure OpenAI service health
- Review token limits in your Azure quota

### Image Generation Failures

**Problem**: Presentations generate but images are missing

**Solution**:
- Verify Pexels API key is valid
- Check Pexels quota (200 requests/hour free tier)
- Alternative: Use `IMAGE_PROVIDER="disabled"` to skip images

## Container Management

### Stop the Container
```bash
docker stop presenton
```

### Start the Container
```bash
docker start presenton
```

### Remove the Container
```bash
docker stop presenton
docker rm presenton
```

### Update to Latest Version
```bash
docker pull othmank/presenton-azure:latest
docker stop presenton
docker rm presenton
# Run the container again with the new image
```

### Access Container Shell (Debug)
```bash
docker exec -it presenton bash
```

## Data Persistence

The container stores presentation data in `/app_data`. The run command mounts `./app_data` from your host:

```bash
-v "./app_data:/app_data"
```

This means presentations are saved to a local `app_data` folder and persist even if you remove the container.

To use a different location:
```bash
-v "/path/to/my/presentations:/app_data"
```

## Security Notes

1. **API Keys**: Keep API keys secure. Set `CAN_CHANGE_KEYS="false"` to prevent users from modifying them.
2. **Network**: This deployment exposes port 5000. For production, consider adding authentication or using a reverse proxy.
3. **Updates**: Check Docker Hub for updates: https://hub.docker.com/r/othmank/presenton-azure

## Technical Details

### Modified Components

This image includes the following modifications to the open-source Presenton project:

1. **Azure OpenAI Native Client**: Uses AsyncAzureOpenAI with legacy API format
2. **Model Validation Skip**: Handles Azure endpoints without /models endpoint
3. **GPT-5 Chat Completions**: Converted from Responses API to Chat Completions API
4. **Token Limits**: Increased to 16000 for GPT-5 reasoning tokens
5. **Dual Model Support**: Environment-based model selection for performance

### Source Code

For technical details and source code modifications, see:
- Full documentation: `AZURE_README.md` in the repository
- Docker Hub: https://hub.docker.com/r/othmank/presenton-azure
- Base project: https://github.com/presenton/presenton

### License

This image is based on Presenton (Apache 2.0 licensed). All modifications maintain the same license.

## Support

For issues or questions:
1. Check Docker Hub: https://hub.docker.com/r/othmank/presenton-azure
2. Review logs: `docker logs presenton`
3. Contact: Othman Kharoubi (othmank@checkpoint.com)

---

**Version**: 1.0.0  
**Last Updated**: January 2026  
**Image**: othmank/presenton-azure:latest
