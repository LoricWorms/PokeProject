from django.db import models

# Create your models here.
class Pokemon(models.Model):
    numero = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    typePokemon = models.CharField(max_length=30)
    image = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    pokemons = models.ManyToManyField(Pokemon)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_full(self):
        return self.pokemons.count() >= 5
