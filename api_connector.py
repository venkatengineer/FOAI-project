"""
API Connector & Knowledge Base Loader Module.
Attempts to fetch knowledge base rules and disease definitions from an external API
(e.g., Fildra / Crop Knowledge API) using an API key header.
Falls back to local knowledge_base.json if API is unavailable, unconfigured, or fails.
"""

import json
import os
import requests

LOCAL_KB_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base.json")


def load_knowledge_base(api_url=None, api_key=None):
    """
    Loads the knowledge base.
    Attempts primary load via API; falls back to local JSON if API fails or is not configured.
    
    Returns:
        tuple: (kb_data: dict, source: str)
    """
    api_url = api_url or os.environ.get("CROP_KNOWLEDGE_API_URL")
    api_key = api_key or os.environ.get("CROP_KNOWLEDGE_API_KEY")

    if api_url:
        headers = {"X-Api-Key": api_key} if api_key else {}
        try:
            response = requests.get(api_url, headers=headers, timeout=3)
            if response.status_code == 200:
                kb_data = response.json()
                if "rules" in kb_data and "diseases" in kb_data:
                    return kb_data, "External API"
        except Exception:
            # Silent fallback to local JSON database on network failure/timeout
            pass

    # Fallback to local database
    with open(LOCAL_KB_PATH, "r", encoding="utf-8") as f:
        kb_data = json.load(f)

    return kb_data, "Local Fallback (JSON)"
