"""
Règles du combat Pokémon : joueur contre ordinateur, tour par tour.

- Chaque équipe a 5 Pokémon. Le premier Pokémon encore debout combat.
- À chaque tour, le joueur choisit :
    * "normale"   : attaque qui touche toujours ;
    * "puissante" : dégâts x2, mais une chance sur deux de rater.
- Ensuite l'ordinateur riposte avec une attaque normale.
- Un Pokémon à 0 PV est K.O. : le suivant de l'équipe prend sa place.
- L'équipe qui n'a plus de Pokémon debout a perdu.
"""

import random


def creer_combattant(pokemon):
    """Copie les infos utiles d'un Pokémon de la base dans un dictionnaire."""
    return {
        "nom": pokemon.nom,
        "image_url": pokemon.image_url,
        "attaque": pokemon.attaque,
        "defense": pokemon.defense,
        "pv_max": pokemon.pv * 2,
        "pv": pokemon.pv * 2,
    }


def nouveau_combat(equipe_joueur, equipe_ia):
    """Prépare un combat entre deux listes de Pokémon."""
    return {
        "joueur": [creer_combattant(p) for p in equipe_joueur],
        "ia": [creer_combattant(p) for p in equipe_ia],
        "journal": ["Le combat commence !"],
        "gagnant": None,
    }


def pokemon_actif(equipe):
    """Renvoie le premier Pokémon encore debout, ou None si tous sont K.O."""
    for pokemon in equipe:
        if pokemon["pv"] > 0:
            return pokemon
    return None


def attaquer(attaquant, defenseur, puissante, journal):
    """L'attaquant frappe le défenseur et on note ce qui se passe."""
    if puissante and random.random() < 0.5:
        journal.append(f"{attaquant['nom']} rate son attaque puissante !")
        return

    degats = round(10 * attaquant["attaque"] / defenseur["defense"])
    if puissante:
        degats = degats * 2
    degats = max(1, degats)

    defenseur["pv"] = max(0, defenseur["pv"] - degats)
    journal.append(f"{attaquant['nom']} inflige {degats} dégâts à {defenseur['nom']}.")
    if defenseur["pv"] == 0:
        journal.append(f"{defenseur['nom']} est K.O. !")


def jouer_tour(combat, action):
    """Le joueur attaque, puis l'ordinateur riposte s'il a encore un Pokémon."""
    journal = combat["journal"]

    # 1. Attaque du joueur
    attaquer(pokemon_actif(combat["joueur"]), pokemon_actif(combat["ia"]),
             action == "puissante", journal)
    if pokemon_actif(combat["ia"]) is None:
        combat["gagnant"] = "joueur"
        journal.append("Victoire ! Toute l'équipe adverse est K.O.")
        return

    # 2. Riposte de l'ordinateur
    attaquer(pokemon_actif(combat["ia"]), pokemon_actif(combat["joueur"]),
             False, journal)
    if pokemon_actif(combat["joueur"]) is None:
        combat["gagnant"] = "ia"
        journal.append("Défaite... Toute votre équipe est K.O.")
