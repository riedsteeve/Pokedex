import random

from django.shortcuts import redirect, render

from .combat import jouer_tour, nouveau_combat, pokemon_actif
from .models import Equipe, Pokemon


def combat(request):
    """Page du combat. L'état du combat est gardé dans la session du joueur."""
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "nouveau":
            # Le joueur choisit une de ses équipes ; l'ordinateur reçoit 5 Pokémon au hasard.
            equipe = Equipe.objects.filter(id=request.POST.get("equipe")).first()
            if equipe:
                equipe_ia = random.sample(list(Pokemon.objects.all()), 5)
                request.session["combat"] = nouveau_combat(equipe.pokemons.all(), equipe_ia)

        elif action == "abandon":
            request.session.pop("combat", None)

        elif action in ("normale", "puissante"):
            partie = request.session.get("combat")
            if partie and not partie["gagnant"]:
                jouer_tour(partie, action)
                request.session["combat"] = partie

        # On redirige pour qu'un rafraîchissement de page ne rejoue pas le tour.
        return redirect("combat")

    partie = request.session.get("combat")
    contexte = {
        "partie": partie,
        "equipes": Equipe.objects.order_by("-id"),
        "assez_de_pokemon": Pokemon.objects.count() >= 5,
    }
    if partie:
        contexte["actif_joueur"] = pokemon_actif(partie["joueur"])
        contexte["actif_ia"] = pokemon_actif(partie["ia"])
        contexte["journal"] = list(reversed(partie["journal"][-8:]))
    return render(request, "combat.html", contexte)
