from django.test import TestCase
from django.urls import reverse

from .combat import attaquer, jouer_tour, nouveau_combat, pokemon_actif
from .models import Equipe, Pokemon


class CombatTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        for i in range(1, 11):
            Pokemon.objects.create(
                pokemon_id=i, nom=f"Pokemon{i}", type1="normal",
                pv=40 + i, attaque=50 + i, defense=45, vitesse=50,
                image_url=f"https://example.com/{i}.png",
            )

    def test_degats_normaux(self):
        partie = nouveau_combat(Pokemon.objects.all()[:5], Pokemon.objects.all()[5:10])
        cible = partie["ia"][0]
        pv_avant = cible["pv"]
        attaquer(partie["joueur"][0], cible, False, partie["journal"])
        self.assertLess(cible["pv"], pv_avant)

    def test_pokemon_ko_remplace_par_le_suivant(self):
        partie = nouveau_combat(Pokemon.objects.all()[:5], Pokemon.objects.all()[5:10])
        partie["ia"][0]["pv"] = 0
        self.assertEqual(pokemon_actif(partie["ia"]), partie["ia"][1])

    def test_combat_complet_se_termine(self):
        partie = nouveau_combat(Pokemon.objects.all()[:5], Pokemon.objects.all()[5:10])
        for _ in range(1000):
            if partie["gagnant"]:
                break
            jouer_tour(partie, "normale")
        self.assertIn(partie["gagnant"], ("joueur", "ia"))

    def test_page_combat(self):
        url = reverse("combat")
        self.assertEqual(self.client.get(url).status_code, 200)

        equipe = Equipe.objects.create(nom="Test")
        equipe.pokemons.set(Pokemon.objects.all()[:5])
        self.client.post(url, {"action": "nouveau", "equipe": equipe.id})
        self.assertIsNotNone(self.client.session.get("combat"))

        for _ in range(1000):
            if self.client.session["combat"]["gagnant"]:
                break
            self.client.post(url, {"action": "puissante"})
        self.assertIsNotNone(self.client.session["combat"]["gagnant"])

        reponse = self.client.get(url)
        self.assertContains(reponse, "Nouveau combat")

        # "Nouveau combat" efface la partie et revient au choix de l'équipe
        self.client.post(url, {"action": "abandon"})
        self.assertIsNone(self.client.session.get("combat"))
        self.assertContains(self.client.get(url), "Lancer le combat")
