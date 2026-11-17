from django.core.management.base import BaseCommand
from pokédex.models import Pokemon
import requests


class Command(BaseCommand):
    help = "Importe les 251 premiers Pokémon depuis PokeAPI"

    
    def handle(self, *args, **kwargs):

        for pokemon_id in range(1, 252):

            self.stdout.write(f"Import du Pokémon {pokemon_id}")

            url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
            response = requests.get(url)

            if response.status_code != 200:
                continue

            data = response.json()

            types = [t["type"]["name"] for t in data["types"]]
            # Mise à jour ou création du Pokémon dans la base de données
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

        self.stdout.write(
            self.style.SUCCESS("Import terminé avec succès !")
        )