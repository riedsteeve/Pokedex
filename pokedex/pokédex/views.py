from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .models import Equipe, Pokemon
from .services import create_pokemon_team, get_all_pokemon, get_pokemon_by_name


def home(request):
    """Liste des Pokémon, 20 par page, avec une recherche par nom."""
    recherche = request.GET.get("q", "").strip()
    if recherche:
        pokemons = get_pokemon_by_name(recherche).order_by("pokemon_id")
    else:
        pokemons = get_all_pokemon().order_by("pokemon_id")

    page = Paginator(pokemons, 20).get_page(request.GET.get("page"))
    return render(request, "home.html", {"page": page, "recherche": recherche})


def detail(request, pokemon_id):
    """Fiche d'un Pokémon, avec des liens vers le précédent et le suivant."""
    pokemon = get_object_or_404(Pokemon, pokemon_id=pokemon_id)
    precedent = Pokemon.objects.filter(pokemon_id__lt=pokemon_id).order_by("-pokemon_id").first()
    suivant = Pokemon.objects.filter(pokemon_id__gt=pokemon_id).order_by("pokemon_id").first()
    return render(request, "detail.html", {
        "pokemon": pokemon,
        "precedent": precedent,
        "suivant": suivant,
    })


def equipes(request):
    """Affiche les équipes enregistrées et permet d'en créer une nouvelle."""
    erreur = None

    if request.method == "POST":
        nom = request.POST.get("nom", "").strip()
        # Les 5 menus déroulants envoient chacun un numéro de Pokémon.
        numeros = [request.POST.get(f"pokemon{i}") for i in range(1, 6)]
        numeros = [int(n) for n in numeros if n]
        equipe = create_pokemon_team(numeros)

        if not nom:
            erreur = "Donnez un nom à votre équipe."
        elif len(equipe) != 5 or len(set(numeros)) != 5:
            erreur = "Choisissez 5 Pokémon différents."
        else:
            nouvelle = Equipe.objects.create(nom=nom)
            nouvelle.pokemons.set(equipe)
            return redirect("equipes")

    return render(request, "equipes.html", {
        "equipes": Equipe.objects.prefetch_related("pokemons").order_by("-id"),
        "tous_les_pokemons": Pokemon.objects.order_by("pokemon_id"),
        "erreur": erreur,
    })


def supprimer_equipe(request, equipe_id):
    """Supprime une équipe (uniquement via le bouton du formulaire)."""
    if request.method == "POST":
        get_object_or_404(Equipe, id=equipe_id).delete()
    return redirect("equipes")
