from django.db import models

# Create your models here.
class Pokemon(models.Model):
    numero = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    typePokemon = models.CharField(max_length=30)
    image = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name