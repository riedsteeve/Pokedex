from django.db import models

class Pokemon(models.Model):
    pokemon_id = models.IntegerField(unique=True)
    nom = models.CharField(max_length=100)

    type1 = models.CharField(max_length=50)
    type2 = models.CharField(max_length=50, blank=True, null=True)

    pv = models.IntegerField()
    attaque = models.IntegerField()
    defense = models.IntegerField()
    vitesse = models.IntegerField()
    image_url = models.URLField()

    def __str__(self):
        return self.nom

class Equipe(models.Model):
    """Une équipe de 5 Pokémon créée par l'utilisateur."""
    nom = models.CharField(max_length=100)
    pokemons = models.ManyToManyField(Pokemon)

    def __str__(self):
        return self.nom
