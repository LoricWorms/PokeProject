import requests
import json
import random

from django.shortcuts import render , redirect
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

def add_to_team(request, id):
    team = request.session.get('team', [])

    if id not in team and len(team) < 5:
        team.append(id)
        request.session['team'] = team

    return redirect('pokemon', id=id)


def remove_from_team(request, id):
    team = request.session.get('team', [])

    if id in team:
        team.remove(id)
        request.session['team'] = team

    return redirect('team')


def team_view(request):
    team_ids = request.session.get('team', [])
    team_pokemons = []

    for pid in team_ids:
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pid}/')
        if response.status_code == 200:
            data = response.json()
            team_pokemons.append({
                'id': data['id'],
                'name': data['name'],
                'image': data['sprites']['front_default'],
                'hp': data['stats'][0]['base_stat'],
                'attack': data['stats'][1]['base_stat'],
                'defense': data['stats'][2]['base_stat'],
            })

    return render(request, 'pokeApp/team.html', {
        'team': team_pokemons
    })
    
def battle(request):
    team_ids = request.session.get('team', [])

    if not team_ids:
        return redirect('team')

    # Initialisation combat
    if 'battle' not in request.session:
        player_team = []
        for pid in team_ids:
            data = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pid}/').json()
            player_team.append({
                'id': pid,
                'name': data['name'],
                'hp': data['stats'][0]['base_stat'],
                'max_hp': data['stats'][0]['base_stat'],
                'attack': data['stats'][1]['base_stat'],
                'defense': data['stats'][2]['base_stat'],
                'image': data['sprites']['front_default'],
                'alive': True,
                'attacks': [
                    {'name': m['move']['name'], 'power': random.randint(10, 25)}
                    for m in data['moves'][:3]
                ]
            })

        enemy_id = random.randint(1, 251)
        enemy_data = requests.get(f'https://pokeapi.co/api/v2/pokemon/{enemy_id}/').json()

        request.session['battle'] = {
            'player_team': player_team,
            'current': 0,
            'enemy': {
                'name': enemy_data['name'],
                'hp': enemy_data['stats'][0]['base_stat'],
                'attack': enemy_data['stats'][1]['base_stat'],
                'defense': enemy_data['stats'][2]['base_stat'],
                'image': enemy_data['sprites']['front_default']
            },
            'message': ''
        }

    battle = request.session['battle']
    current = battle['current']
    player = battle['player_team'][current]
    enemy = battle['enemy']

    combat_fini = False

    if request.method == "POST" and player['alive']:
        power = int(request.POST['attack'])
        dmg = max(1, power + player['attack'] - enemy['defense'] // 2)
        enemy['hp'] -= dmg
        battle['message'] = f"{player['name']} inflige {dmg} dégâts !"

        if enemy['hp'] <= 0:
            battle['message'] += " Ennemi vaincu !"
            combat_fini = True

        else:
            dmg_enemy = max(1, enemy['attack'] - player['defense'] // 2)
            player['hp'] -= dmg_enemy

            if player['hp'] <= 0:
                player['alive'] = False
                battle['message'] += f" {player['name']} est KO !"

                # chercher leprochain Pokémon vivant
                for i, p in enumerate(battle['player_team']):
                    if p['alive']:
                        battle['current'] = i
                        break
                else:
                    battle['message'] += " Défaite !"
                    combat_fini = True

    request.session['battle'] = battle

    return render(request, 'pokeApp/battle.html', {
        'player': player,
        'enemy': enemy,
        'player_hp': player['hp'],
        'enemy_hp': enemy['hp'],
        'attacks': player['attacks'],
        'message': battle['message'],
        'combat_fini': combat_fini
    })
