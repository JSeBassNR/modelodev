import os
import requests
from typing import Any

API1_URL = os.environ.get('API1_URL')
API2_URL = os.environ.get('API2_URL')
API_KEY = os.environ.get('API_KEY')
# Optional base URL for the Ganadero Spring Boot service discovered in your Java sources
GANADERO_BASE_URL = os.environ.get('GANADERO_API_URL')  # e.g. http://localhost:8080/api/ganadero


def _headers():
    headers = {'Content-Type': 'application/json'}
    if API_KEY:
        headers['Authorization'] = f'Bearer {API_KEY}'
    return headers


def send_image_summary(payload: Any, url: str = None):
    target = url or API1_URL
    if not target:
        return None
    try:
        r = requests.post(target, json=payload, headers=_headers(), timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def send_alert(payload: Any, url: str = None):
    target = url or API2_URL
    if not target:
        return None
    try:
        r = requests.post(target, json=payload, headers=_headers(), timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


# --- Generated client functions for GanaderoController (Spring Boot)
def ganadero_headers():
    headers = {'Content-Type': 'application/json'}
    if API_KEY:
        headers['Authorization'] = f'Bearer {API_KEY}'
    return headers


def create_ganadero(payload: Any, base_url: str = None):
    """POST /save -> creates a Ganadero. Returns JSON or None on failure."""
    target = (base_url or GANADERO_BASE_URL or '').rstrip('/') + '/save'
    if not target or target == '/save':
        return None
    try:
        r = requests.post(target, json=payload, headers=ganadero_headers(), timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def get_ganadero_by_id(ganadero_id: int, base_url: str = None):
    """GET /{id} -> returns Ganadero JSON or None"""
    base = base_url or GANADERO_BASE_URL
    if not base:
        return None
    target = f"{base.rstrip('/')}/{ganadero_id}"
    try:
        r = requests.get(target, headers=ganadero_headers(), timeout=10)
        if r.status_code == 200:
            return r.json()
        return None
    except Exception:
        return None


def update_ganadero(payload: Any, base_url: str = None):
    """PUT /update -> updates a Ganadero (expects GanaderoData body). Returns JSON or None."""
    target = (base_url or GANADERO_BASE_URL or '').rstrip('/') + '/update'
    if not target or target == '/update':
        return None
    try:
        r = requests.put(target, json=payload, headers=ganadero_headers(), timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def delete_ganadero(ganadero_id: int, base_url: str = None):
    """DELETE /delete/{id} -> returns True if deleted, False otherwise."""
    base = base_url or GANADERO_BASE_URL
    if not base:
        return False
    target = f"{base.rstrip('/')}/delete/{ganadero_id}"
    try:
        r = requests.delete(target, headers=ganadero_headers(), timeout=10)
        return r.status_code == 200
    except Exception:
        return False


def find_ganadero_by_email(email: str, base_url: str = None):
    """GET /buscar-email/{email} -> returns Ganadero JSON or None"""
    base = base_url or GANADERO_BASE_URL
    if not base:
        return None
    target = f"{base.rstrip('/')}/buscar-email/{email}"
    try:
        r = requests.get(target, headers=ganadero_headers(), timeout=10)
        if r.status_code == 200:
            return r.json()
        return None
    except Exception:
        return None


def get_ganaderos_paged(page: int = 0, size: int = 10, base_url: str = None):
    """GET /all?page=&size= -> returns page JSON or None"""
    base = base_url or GANADERO_BASE_URL
    if not base:
        return None
    target = f"{base.rstrip('/')}/all"
    params = {'page': page, 'size': size}
    try:
        r = requests.get(target, params=params, headers=ganadero_headers(), timeout=10)
        if r.status_code == 200:
            return r.json()
        return None
    except Exception:
        return None
