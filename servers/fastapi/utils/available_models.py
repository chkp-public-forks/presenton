from anthropic import AsyncAnthropic
from openai import AsyncOpenAI
from google import genai


async def list_available_openai_compatible_models(url: str, api_key: str) -> list[str]:
    try:
        # Check if this is Azure OpenAI (needs api-key header)
        default_headers = {}
        if "azure" in url.lower():
            default_headers = {"api-key": api_key}
        
        client = AsyncOpenAI(api_key=api_key, base_url=url, default_headers=default_headers)
        models = (await client.models.list()).data
        if models:
            return list(map(lambda x: x.id, models))
        return []
    except Exception as e:
        # If models.list() fails (e.g., Azure OpenAI gateway without /models endpoint),
        # skip validation and allow the user to proceed with their configured model
        print(f"Warning: Could not fetch available models from {url}: {e}")
        print("Proceeding without model validation...")
        return []


async def list_available_anthropic_models(api_key: str) -> list[str]:
    client = AsyncAnthropic(api_key=api_key)
    return list(map(lambda x: x.id, (await client.models.list(limit=50)).data))


async def list_available_google_models(api_key: str) -> list[str]:
    client = genai.Client(api_key=api_key)
    return list(map(lambda x: x.name, client.models.list(config={"page_size": 50})))
