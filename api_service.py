import requests

BASE_URL = "https://brasil.io/api/dados-juridicos"

def buscar_decisoes(keyword, page=1):
    url = f"{BASE_URL}/decisions"
    params = {"search": keyword, "page": page}
    r = requests.get(url, params=params)

    if r.status_code != 200:
        return None

    return r.json()
