import requests
from .models import Pokemon, Team
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.shortcuts import render



# Create your views here.
def index(request):
    response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1025')
    pokemon_list = []
    if response.status_code == 200:
        results = response.json()['results']
        for i, pokemon in enumerate(results):
            pokemon_list.append({
                'name': pokemon['name'],
                'id': i + 1,
                'image': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{i + 1}.png"
            })
    
    context = {
        'title' : 'Bienvenue sur mon Pokédex !',
        'pokemon_list': pokemon_list
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


def create_team(request):
    team, created = Team.objects.get_or_create(name="Mon équipe")
    return redirect('index')


def add_to_team(request, pokemon_id):
    team = Team.objects.get(name="Mon équipe")
    pokemon = get_object_or_404(Pokemon, numero=pokemon_id)

    if team.is_full():
        return HttpResponse("Équipe complète (5 Pokémon max)")

    team.pokemons.add(pokemon)
    return redirect('pokemon', id=pokemon_id)


def team_view(request):
    team, created = Team.objects.get_or_create(name="Mon équipe")

    context = {
        'team': team,
        'pokemons': team.pokemons.all()
    }
    return render(request, 'pokeApp/team.html', context)
