class Team:
    def __init__(self, name="Equipe"):
        self.name = name
        self.pokemons = []

    def add_pokemon(self, pokemon):
        if len(self.pokemons) >= 5:
            raise ValueError("Une équipe ne peut pas avoir plus de 5 Pokémon")
        if pokemon in self.pokemons:
            raise ValueError("Ce Pokémon est déjà dans l'équipe")
        self.pokemons.append(pokemon)

    def remove_pokemon(self, pokemon):
        self.pokemons.remove(pokemon)

    def is_full(self):
        return len(self.pokemons) == 5

    def __str__(self):
        return f"{self.name} ({len(self.pokemons)}/5)"
