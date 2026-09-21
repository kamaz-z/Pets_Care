import requests
from django.http import JsonResponse
from django.conf import settings

NOVAPOST_API_KEY = "ТВІЙ_API_КЛЮЧ_З_КАБІНЕТУ"
BASE_URL = "https://api.novapost.com/v.1.0"

def search_settlements(request):
    """Пошук міст для інпуту"""
    query = request.GET.get('q', '')
    
    headers = {
        "Authorization": NOVAPOST_API_KEY,
        "Accept": "application/json"
    }
    
    params = {
        "countryCodes[]": "UA",
        "textSearch": query,
        "limit": 10
    }
    
    response = requests.get(f"{BASE_URL}/settlements", headers=headers, params=params)
    return JsonResponse(response.json())


def get_divisions(request, settlement_id):
    """Отримання відділень для вибраного міста"""
    headers = {
        "Authorization": NOVAPOST_API_KEY,
        "Accept": "application/json"
    }
    
    params = {
        "countryCodes[]": "UA",
        "settlementIds[]": settlement_id,
        "limit": 100
    }
    
    response = requests.get(f"{BASE_URL}/divisions", headers=headers, params=params)
    return JsonResponse(response.json())