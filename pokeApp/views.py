import requests
import json
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def index(request):
    # Récupérer la liste des générations
    generations_response = requests.get('https://pokeapi.co/api/v2/generation')
    generations = generations_response.json()['results'] if generations_response.status_code == 200 else []

    all_pokemon_list = []
    selected_generation = request.GET.get('generation')

    if selected_generation:
        # Si une génération est sélectionnée, récupérer les Pokémon de cette génération
        response = requests.get(f'https://pokeapi.co/api/v2/generation/{selected_generation}/')
        if response.status_code == 200:
            pokemon_species = response.json()['pokemon_species']
            for species in pokemon_species:
                # Extraire l'ID du Pokémon de l'URL de l'espèce
                pokemon_id = species['url'].split('/')[-2]
                all_pokemon_list.append({
                    'name': species['name'],
                    'id': pokemon_id,
                    'image': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"
                })
    else:
        # Comportement par défaut : récupérer tous les Pokémon
        response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1025')
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
        pokemon_list_filtered = [
            pokemon for pokemon in all_pokemon_list
            if search_query.lower() in pokemon['name'].lower()
        ]
    else:
        pokemon_list_filtered = all_pokemon_list

    paginator = Paginator(pokemon_list_filtered, 25)  # 25 Pokémons par page
    page_number = request.GET.get('page')
    try:
        pokemon_page = paginator.get_page(page_number)
    except PageNotAnInteger:
        pokemon_page = paginator.page(1)
    except EmptyPage:
        pokemon_page = paginator.page(paginator.num_pages)

    context = {
        'title': 'Bienvenue sur mon Pokédex !',
        'pokemon_list': pokemon_page,
        'search_query': search_query if search_query is not None else '',
        'generations': generations,
        'selected_generation': int(selected_generation) if selected_generation else None,
    }
    return render(request, 'pokeApp/index.html', context)

def pokemon(request, id):
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{id}/')
    poke_data = response.json()
    
    types = [t['type']['name'] for t in poke_data['types']]
    
    stats = {
        'names': json.dumps([s['stat']['name'] for s in poke_data['stats']]),
        'values': json.dumps([s['base_stat'] for s in poke_data['stats']])
    }

    context = {
        'number' : poke_data['id'],
        'name' : poke_data['name'],
        'type' : ', '.join(types),
        'height': poke_data['height'],
        'weight': poke_data['weight'],
        'img' : poke_data['sprites']['front_default'],
        'stats': stats
    } 
    return render(request, 'pokeApp/pokemon.html', context)