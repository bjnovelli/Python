import requests

def fetch_data(endpoint, filters={}):
    url = f"https://rickandmortyapi.com/api/{endpoint}"  # Corrigida a barra
    response = requests.get(url, params=filters)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao buscar dados: {response.status_code}")
        return None

# Busca personagens com nome "Rick"
characters = fetch_data("character", {"name": "Rick"})

# Exibe nomes dos personagens encontrados
if characters and "results" in characters:
    print("Personagens encontrados:")
    for c in characters["results"]:
        print(f"- {c['name']}")
else:
    print("Nenhum personagem encontrado ou erro na requisição.")
