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
    
    
    team = request.session.get('team', [])
    in_team = id in team
    
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
        'stats': stats,
        'in_team': in_team
    } 
    return render(request, 'pokeApp/pokemon.html', context)

def add_to_team(request, id):
    team = request.session.get('team', [])

    if id not in team and len(team) < 5:
        team.append(id)
        request.session['team'] = team

    return redirect('team')


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
    
    if request.method == "GET" and 'battle' in request.session: 
        del request.session['battle']

    if 'team' not in request.session or not request.session['team']:
        return redirect('team')

    # initialisation du combat
    if 'battle' not in request.session:
        player_team = []
        for pid in request.session['team']:
            p = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pid}/').json()
            player_team.append({
                'id': pid,
                'name': p['name'],
                'hp': p['stats'][0]['base_stat'],
                'max_hp': p['stats'][0]['base_stat'],
                'attack': p['stats'][1]['base_stat'],
                'defense': p['stats'][2]['base_stat'],
                'image': p['sprites']['front_default'],
                'alive': True,
                'attacks': [
                    {'name': m['move']['name'], 'power': random.randint(10, 25)}
                    for m in p['moves'][:4]
                ]
            })

        enemy_team = []
        for _ in range(len(player_team)):
            eid = random.randint(1, 251)
            e = requests.get(f'https://pokeapi.co/api/v2/pokemon/{eid}/').json()
            enemy_team.append({
                'name': e['name'],
                'hp': e['stats'][0]['base_stat'],
                'max_hp': e['stats'][0]['base_stat'],
                'attack': e['stats'][1]['base_stat'],
                'defense': e['stats'][2]['base_stat'],
                'image': e['sprites']['front_default'],
                'alive': True
            })

        request.session['battle'] = {
            'player_team': player_team,
            'enemy_team': enemy_team,
            'player_current': 0,
            'enemy_current': 0,
            'message': '',
            'combat_fini': False,  
        }

    battle = request.session['battle']
    player = battle['player_team'][battle['player_current']]
    enemy = battle['enemy_team'][battle['enemy_current']]

    # Vérrif pour voir si le combat est déjà fini
    if not any(p['alive'] for p in battle['player_team']):
        battle['message'] = "Défaite : votre équipe est KO"
        battle['combat_fini'] = True
    elif not any(e['alive'] for e in battle['enemy_team']):
        battle['message'] = "Victoire : équipe ennemie vaincue"
        battle['combat_fini'] = True

    # Si le combat est fini, on ne fait rien d'autre
    if not battle.get('combat_fini', False):

        # changer de Pokémon
        if request.method == "POST" and 'switch' in request.POST:
            idx = int(request.POST['switch'])
            if battle['player_team'][idx]['alive']:
                battle['player_current'] = idx
                player = battle['player_team'][battle['player_current']]

        # attaque
        elif request.method == "POST" and 'attack' in request.POST:

            # empêcher un Pokémon KO d’attaquer
            if not player['alive'] or player['hp'] <= 0:
                battle['message'] = f"{player['name']} est KO et ne peut pas attaquer."
            elif not enemy['alive'] or enemy['hp'] <= 0:
                battle['message'] = f"{enemy['name']} est déjà KO."
            else:
                #dégats
                power = int(request.POST['attack'])
                
                dmg = max(1, power + player['attack'] - enemy['defense'] // 2)
                enemy['hp'] = max(0, enemy['hp'] - dmg)
                battle['message'] = f"{player['name']} attaque ({dmg} dégâts)"

                if enemy['hp'] <= 0:
                    enemy['alive'] = False
                    battle['message'] += f" → {enemy['name']} est KO"

                    # chercher un nouvel ennemi vivant, parmi la liste
                    for i, e in enumerate(battle['enemy_team']):
                        if e['alive']:
                            battle['enemy_current'] = i
                            enemy = battle['enemy_team'][i]
                            break
                else:
                    # riposte de l’ennemi uniquement s’il est encore vivant
                    dmg_enemy = max(1, enemy['attack'] - player['defense'] // 2)
                    player['hp'] = max(0, player['hp'] - dmg_enemy)

                    if player['hp'] <= 0:
                        player['alive'] = False
                        battle['message'] += f" → {player['name']} est KO"

                        # chercher un nouveau Pokémon vivant côté joueur
                        for i, p in enumerate(battle['player_team']):
                            if p['alive']:
                                battle['player_current'] = i
                                player = battle['player_team'][i]
                                break

        
        if not any(p['alive'] for p in battle['player_team']):
            battle['message'] = "Défaite : votre équipe est KO"
            battle['combat_fini'] = True
        elif not any(e['alive'] for e in battle['enemy_team']):
            battle['message'] = "Victoire : équipe ennemie vaincue"
            battle['combat_fini'] = True

    request.session['battle'] = battle
    
    # Calcul des pourcentages pr la barre de vie
    player['hp_percent'] = int((player['hp'] / player['max_hp']) * 100)
    enemy['hp_percent'] = int((enemy['hp'] / enemy['max_hp']) * 100)

    for p in battle['player_team']:
        p['hp_percent'] = int((p['hp'] / p['max_hp']) * 100)

    for e in battle['enemy_team']:
        e['hp_percent'] = int((e['hp'] / e['max_hp']) * 100)


    return render(request, 'pokeApp/battle.html', {
        'player': player,
        'enemy': enemy,
        'player_team': battle['player_team'],
        'enemy_team': battle['enemy_team'],
        'attacks': player['attacks'],
        'message': battle['message'],
        'combat_fini': battle.get('combat_fini', False),
        'player_hp': player['hp'],
        'enemy_hp': enemy['hp'],
    })

