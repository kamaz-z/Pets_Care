import requests

def get_cities():
    response = requests.get(
    "https://api-stage.novapost.com//v.1.0/clients/authorization?apiKey=text",
    headers={"Accept":"*/*"},)

    data = response.json()
    return data
    
