from .models import Pokemon

def get_all_pokemon():
    return Pokemon.objects.all()

def get_pokemon_by_name(name):
    return Pokemon.objects.filter(nom__icontains=name)

def get_pokemon_by_type(type_name):
    return Pokemon.objects.filter(type1__iexact=type_name)

def get_pokemon_image_url(pokemon_id):
    try:
        pokemon = Pokemon.objects.get(pokemon_id=pokemon_id)
        return pokemon.image_url
    except Pokemon.DoesNotExist:
        return None


#Crée une équipe de 5 pokémon
def create_pokemon_team(pokemon_ids):
    team = []
    for pokemon_id in pokemon_ids:
        try:
            pokemon = Pokemon.objects.get(pokemon_id=pokemon_id)
            team.append(pokemon)
        except Pokemon.DoesNotExist:
            continue
    return team
