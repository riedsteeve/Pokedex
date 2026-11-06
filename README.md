# Pokédex

## Prérequis

- Python 3.12 ou plus récent
- Node.js 22 ou plus récent et npm

## Installation

Depuis la racine du dépôt, sur macOS/Linux :

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cd pokedex
../.venv/bin/python manage.py tailwind install
../.venv/bin/python manage.py migrate
```

- `venv` crée un environnement Python isolé pour le projet.
- `pip install` installe Django et les dépendances Python listées dans le fichier.
- `cd pokedex` entre dans le dossier qui contient `manage.py`.
- `tailwind install` installe les dépendances npm et compile le CSS Tailwind.
- `migrate` prépare la base de données locale.

Sur Windows PowerShell, depuis la racine du dépôt :

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
cd pokedex
..\.venv\Scripts\python.exe manage.py tailwind install
..\.venv\Scripts\python.exe manage.py migrate
```

Ces commandes font les mêmes étapes que celles de macOS/Linux, avec le chemin
de l’exécutable Python adapté à PowerShell.

## Lancement en développement

Ouvre deux terminaux à la racine du dépôt.

Terminal 1, pour compiler Tailwind pendant le développement :

```bash
cd pokedex
../.venv/bin/python manage.py tailwind start
```

Cette commande surveille les fichiers et recompile Tailwind après chaque
modification.

Dans PowerShell, remplace cette commande par
`..\.venv\Scripts\python.exe manage.py tailwind start`.

Terminal 2, pour lancer Django :

```bash
cd pokedex
../.venv/bin/python manage.py runserver
```

Cette commande démarre le serveur Django pour consulter le site dans le
navigateur.

Dans PowerShell, remplace cette commande par
`..\.venv\Scripts\python.exe manage.py runserver`.

Ouvre ensuite <http://127.0.0.1:8000/>.

## Sécurité

La configuration fournie est réservée au développement (`DEBUG = True` et clé
de développement). Ne l’utilise pas telle quelle en production.