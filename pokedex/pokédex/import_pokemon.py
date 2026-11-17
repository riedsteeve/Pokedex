import os
import django
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pokedex.settings")
django.setup()

from .models import Pokemon


def import_pokemon():
    for pokemon_id in range(1, 252):

        print(f"Import du Pokémon {pokemon_id}")

        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Erreur pour le Pokémon {pokemon_id}")
            continue

        data = response.json()

        types = [t["type"]["name"] for t in data["types"]]

        Pokemon.objects.update_or_create(
            pokemon_id=pokemon_id,
            defaults={
                "nom": data["name"].capitalize(),
                "type1": types[0],
                "type2": types[1] if len(types) > 1 else None,
                "pv": data["stats"][0]["base_stat"],
                "attaque": data["stats"][1]["base_stat"],
                "defense": data["stats"][2]["base_stat"],
                "vitesse": data["stats"][5]["base_stat"],
                "image_url": data["sprites"]["front_default"],
            }
        )

    print("Import terminé !")


if __name__ == "__main__":
    import_pokemon()