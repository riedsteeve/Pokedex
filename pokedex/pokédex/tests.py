from django.test import TestCase

from .models import Pokemon

# Create your tests here.
from django.test import TestCase
from .models import Pokemon
from .services import (
    get_all_pokemon,
    get_pokemon_by_name,
    get_pokemon_by_type
)

class PokemonTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        Pokemon.objects.create(
            pokemon_id=25,
            nom="Pikachu",
            type1="electric",
            type2=None,
            pv=35,
            attaque=55,
            defense=40,
            vitesse=90,
            image_url="https://example.com/pikachu.png"
        )

        Pokemon.objects.create(
            pokemon_id=6,
            nom="Charizard",
            type1="fire",
            type2="flying",
            pv=78,
            attaque=84,
            defense=78,
            vitesse=100,
            image_url="https://example.com/charizard.png"
        )

    def test_pokemon_creation(self):
        pikachu = Pokemon.objects.get(pokemon_id=25)

        self.assertEqual(pikachu.nom, "Pikachu")
        self.assertEqual(pikachu.type1, "electric")
        self.assertEqual(pikachu.pv, 35)

    def test_get_all_pokemon(self):
        pokemons = get_all_pokemon()

        self.assertEqual(pokemons.count(), 2)

    def test_get_pokemon_by_name_found(self):
        result = get_pokemon_by_name("Pikachu")

        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first().nom, "Pikachu")

    def test_get_pokemon_by_name_not_found(self):
        result = get_pokemon_by_name("Mewthree")

        self.assertEqual(result.count(), 0)

    def test_get_pokemon_by_type_found(self):
        result = get_pokemon_by_type("electric")

        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first().nom, "Pikachu")

    def test_get_pokemon_by_type_not_found(self):
        result = get_pokemon_by_type("dragon")

        self.assertEqual(result.count(), 0)

    def test_image_url_exists(self):
        pikachu = Pokemon.objects.get(pokemon_id=25)

        self.assertIsNotNone(pikachu.image_url)
        self.assertNotEqual(pikachu.image_url, "")

