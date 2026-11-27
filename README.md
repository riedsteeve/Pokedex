# Pokédex — Projet Python B3

Pokédex web réalisé avec **Django**. Il affiche les 251 premiers Pokémon
(récupérés depuis [PokeAPI](https://pokeapi.co/)), permet de les parcourir et de
les rechercher, de composer des équipes de 5 Pokémon et de les faire combattre
contre l'ordinateur.

## Fonctionnalités

| Page | Adresse | Ce qu'on peut faire |
|------|---------|---------------------|
| Pokémon | `/` | Liste des Pokémon (20 par page) avec boutons **Précédent / Suivant** et **recherche par nom** |
| Fiche Pokémon | `/pokemon/<numéro>/` | Image, types et statistiques (PV, attaque, défense, vitesse), liens vers le Pokémon précédent et suivant |
| Équipes | `/equipes/` | Créer une équipe de 5 Pokémon différents, voir et supprimer les équipes enregistrées |
| Combat | `/combat/` | Choisir une de ses équipes et combattre l'ordinateur, tour par tour |

## Prérequis

- **Python 3.12** ou plus récent
- Une connexion Internet (pour l'import des Pokémon et l'affichage des images)

Node.js n'est **pas** nécessaire pour lancer le projet : le CSS est déjà compilé
dans le dépôt. Il ne sert que si l'on modifie le style (voir plus bas).

## Installation

Toutes les commandes se lancent **depuis la racine du dépôt**.

### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
cd pokedex
..\.venv\Scripts\python.exe manage.py migrate
..\.venv\Scripts\python.exe manage.py import_pokemon
```

### macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cd pokedex
../.venv/bin/python manage.py migrate
../.venv/bin/python manage.py import_pokemon
```

Ce que fait chaque commande :

1. `venv` crée un environnement Python isolé pour le projet.
2. `pip install -r requirements.txt` installe Django, django-tailwind et requests.
3. `migrate` crée la base de données SQLite (`pokedex/db.sqlite3`) et ses tables.
4. `import_pokemon` télécharge les 251 premiers Pokémon depuis PokeAPI et les
   enregistre en base (environ 1 à 2 minutes). On peut la relancer sans risque :
   les Pokémon déjà présents sont mis à jour, pas dupliqués.

## Lancement

Depuis le dossier `pokedex` :

```powershell
..\.venv\Scripts\python.exe manage.py runserver      # Windows
```
```bash
../.venv/bin/python manage.py runserver              # macOS / Linux
```

Puis ouvrir <http://127.0.0.1:8000/> dans un navigateur.

**Utilisation conseillée :** parcourir les Pokémon → créer une équipe dans
**Équipes** → lancer un combat dans **Combat**.

## Règles du combat

- L'équipe du joueur (5 Pokémon) affronte une équipe de 5 Pokémon tirés au
  hasard pour l'ordinateur.
- À chaque tour, le joueur choisit son attaque :
  - **Attaque normale** : touche toujours ;
  - **Attaque puissante** : dégâts ×2, mais une chance sur deux de rater.
- L'ordinateur riposte ensuite avec une attaque normale.
- Dégâts = 10 × attaque de l'attaquant ÷ défense du défenseur (minimum 1).
- En combat, un Pokémon a 2 × ses PV de base, pour que les combats durent un
  peu plus longtemps.
- Un Pokémon à 0 PV est K.O. et le suivant de l'équipe le remplace. L'équipe qui
  n'a plus de Pokémon debout a perdu.

## Choix techniques

- **Django** : framework web Python complet (base de données, pages, formulaires)
  qui évite d'avoir à coder une interface graphique de bureau, et rend le
  Pokédex utilisable depuis n'importe quel navigateur.
- **SQLite** : base de données fournie avec Python, sans serveur à installer.
  Les Pokémon sont importés **une seule fois** depuis PokeAPI puis lus en base :
  le site reste rapide et ne dépend pas de l'API pendant l'utilisation (seules
  les images restent hébergées sur les serveurs de PokeAPI).
- **Tailwind CSS** (via django-tailwind) : mise en forme directement dans les
  templates HTML avec des classes prédéfinies.
- **Combat contre l'ordinateur** plutôt que contre un second joueur, pour
  pouvoir jouer seul. L'état du combat est gardé dans la **session Django**
  (pas en base), car il est temporaire. Les règles sont volontairement simples
  et regroupées dans un seul fichier (`combat.py`) indépendant des pages web.
- Les équipes sont reliées aux Pokémon par une relation **ManyToMany** : un
  Pokémon peut appartenir à plusieurs équipes.

## Organisation du code

```
pokedex/                     dossier contenant manage.py
├── pokedex/                 configuration du projet Django
│   ├── settings.py          réglages (applications, base de données…)
│   └── urls.py              adresses du site → vues
├── pokédex/                 application principale
│   ├── models.py            modèles Pokemon et Equipe (tables de la base)
│   ├── management/commands/
│   │   └── import_pokemon.py   commande d'import depuis PokeAPI
│   ├── services.py          fonctions de recherche et de création d'équipe
│   ├── views.py             pages liste, détail et équipes
│   ├── views_combat.py      page de combat
│   ├── combat.py            règles du combat
│   ├── templates/           pages HTML
│   └── test*.py             tests automatiques
└── theme/                   Tailwind CSS et gabarit commun (base.html, menu)
```

## Tests

Depuis le dossier `pokedex` :

```bash
../.venv/bin/python manage.py test pokédex       # macOS / Linux
..\.venv\Scripts\python.exe manage.py test pokédex   # Windows
```

## Modifier le style (optionnel)

Seulement si l'on change des classes CSS dans les templates. Nécessite
**Node.js 22+** :

```bash
../.venv/bin/python manage.py tailwind install   # une seule fois
../.venv/bin/python manage.py tailwind start     # recompile à chaque modification
```

Avant de livrer, `tailwind build` produit la version finale du CSS.

## Équipe

| Rôle | Membre |
|------|--------|
| Données & API | Lise |
| Affichage & recherche | _à compléter_ |
| Gestion des équipes | Steeve |
| Combat & documentation | _à compléter_ |

## Sécurité

La configuration fournie est réservée au développement (`DEBUG = True` et clé
de développement). Elle ne doit pas être utilisée telle quelle en production.
