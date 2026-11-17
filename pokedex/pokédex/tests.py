from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import Pokemon
from .services import (
    create_pokemon_team,
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

        Pokemon.objects.create(
            pokemon_id=7,
            nom="Bulbasaur",
            type1="grass",
            type2="poison",
            pv=45,
            attaque=49,
            defense=49,
            vitesse=45,
            image_url="https://example.com/bulbasaur.png"
        )

        Pokemon.objects.create(
            pokemon_id=8,
            nom="Squirtle",
            type1="water",
            type2=None,
            pv=44,
            attaque=48,
            defense=65,
            vitesse=43,
            image_url="https://example.com/squirtle.png"
        )

        Pokemon.objects.create(
            pokemon_id=150,
            nom="Mewtwo",
            type1="psychic",
            type2=None,
            pv=106,
            attaque=110,
            defense=90,
            vitesse=130,
            image_url="https://example.com/mewtwo.png"
        )

        Pokemon.objects.create(
            pokemon_id=151,
            nom="Mew",
            type1="psychic",
            type2=None,
            pv=100,
            attaque=100,
            defense=100,
            vitesse=100,
            image_url="https://example.com/mew.png"
        )

        Pokemon.objects.create(
            pokemon_id=4,
            nom="Charmander",
            type1="fire",
            type2=None,
            pv=39,
            attaque=52,
            defense=43,
            vitesse=65,
            image_url="https://example.com/charmander.png"
        )
        

    def test_pokemon_creation(self):
        pikachu = Pokemon.objects.get(pokemon_id=25)

        self.assertEqual(pikachu.nom, "Pikachu")
        self.assertEqual(pikachu.type1, "electric")
        self.assertEqual(pikachu.pv, 35)

    def test_get_all_pokemon(self):
        pokemons = get_all_pokemon()

        self.assertEqual(pokemons.count(), 7)

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

#Test de la création d'une équipe de 5 pokémon
    def test_create_pokemon_team(self):
        pokemon_ids = [25, 6, 7, 8, 150]
        team = create_pokemon_team(pokemon_ids)

        self.assertEqual(len(team), 5)
        self.assertEqual(team[0].nom, "Pikachu")
        self.assertEqual(team[1].nom, "Charizard")
        self.assertEqual(team[2].nom, "Bulbasaur")
        self.assertEqual(team[3].nom, "Squirtle")
        self.assertEqual(team[4].nom, "Mewtwo")

        print("Test de création d'équipe de 5 Pokémon réussi !")
        print("Équipe créée :")
        for pokemon in team:
            print(f"- {pokemon.nom} (ID: {pokemon.pokemon_id})")

