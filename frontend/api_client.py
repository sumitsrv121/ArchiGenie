import os
import requests
from typing import Dict

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

class APIError(Exception):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code

def call_api(endpoint: str, payload: Dict) -> Dict:
    url = f"{BACKEND_URL}{endpoint}"
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        error_detail = e.response.json().get("detail", str(e))
        raise APIError(f"API Error [{e.response.status_code}]: {error_detail}", e.response.status_code)
    except requests.exceptions.RequestException as e:
        raise APIError(f"Network error: {str(e)}", 503)

def call_api_get(endpoint: str) -> Dict:
    url = f"{BACKEND_URL}{endpoint}"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        error_detail = e.response.json().get("detail", str(e))
        raise APIError(f"API Error [{e.response.status_code}]: {error_detail}", e.response.status_code)
    except requests.exceptions.RequestException as e:
        raise APIError(f"Network error: {str(e)}", 503)
