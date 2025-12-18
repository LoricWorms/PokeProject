import requests
from django.shortcuts import render

# Create your views here.
def index(request):
    response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1025')
    all_pokemon_list = []
    if response.status_code == 200:
        results = response.json()['results']
        for i, pokemon in enumerate(results):
            all_pokemon_list.append({
                'name': pokemon['name'],
                'id': i + 1,
                'image': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{i + 1}.png"
            })
    
    search_query = request.GET.get('q')
    if search_query:
        pokemon_list = [
            pokemon for pokemon in all_pokemon_list 
            if search_query.lower() in pokemon['name'].lower()
        ]
    else:
        pokemon_list = all_pokemon_list

    context = {
        'title' : 'Bienvenue sur mon Pokédex !',
        'pokemon_list': pokemon_list,
        'search_query': search_query
    }
    return render(request, 'pokeApp/index.html', context)

def pokemon(request, id):
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{id}/')
    poke_data = response.json()
    
    types = [t['type']['name'] for t in poke_data['types']]

    context = {
        'number' : poke_data['id'],
        'name' : poke_data['name'],
        'type' : ', '.join(types),
        'height': poke_data['height'],
        'weight': poke_data['weight'],
        'img' : poke_data['sprites']['front_default']
    } 
    return render(request, 'pokeApp/pokemon.html', context)