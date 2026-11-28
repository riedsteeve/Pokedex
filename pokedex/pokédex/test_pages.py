from django.test import TestCase
from django.urls import reverse

from .models import Equipe, Pokemon


class PagesTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        for i in range(1, 26):
            Pokemon.objects.create(
                pokemon_id=i, nom=f"Pokemon{i}", type1="normal",
                pv=40, attaque=50, defense=45, vitesse=50,
                image_url=f"https://example.com/{i}.png",
            )
        Pokemon.objects.filter(pokemon_id=25).update(nom="Pikachu")

    def test_liste_pagination(self):
        page1 = self.client.get(reverse("home"))
        self.assertContains(page1, "Pokemon1<")
        self.assertNotContains(page1, "Pokemon21<")  # 20 Pokémon par page
        self.assertContains(page1, "Suivant")

        page2 = self.client.get(reverse("home") + "?page=2")
        self.assertContains(page2, "Pokemon21<")
        self.assertContains(page2, "Précédent")

    def test_recherche(self):
        reponse = self.client.get(reverse("home") + "?q=pika")
        self.assertContains(reponse, "Pikachu")
        self.assertNotContains(reponse, "Pokemon1<")

    def test_detail_et_navigation(self):
        reponse = self.client.get(reverse("detail", args=[2]))
        self.assertContains(reponse, "Pokemon2")
        self.assertContains(reponse, reverse("detail", args=[1]))
        self.assertContains(reponse, reverse("detail", args=[3]))

    def test_detail_inexistant(self):
        self.assertEqual(self.client.get(reverse("detail", args=[999])).status_code, 404)

    def test_creer_et_supprimer_equipe(self):
        donnees = {"nom": "Ma team", "pokemon1": 1, "pokemon2": 2,
                   "pokemon3": 3, "pokemon4": 4, "pokemon5": 25}
        self.client.post(reverse("equipes"), donnees)
        equipe = Equipe.objects.get(nom="Ma team")
        self.assertEqual(equipe.pokemons.count(), 5)
        self.assertContains(self.client.get(reverse("equipes")), "Ma team")

        self.client.post(reverse("supprimer_equipe", args=[equipe.id]))
        self.assertFalse(Equipe.objects.exists())

    def test_equipe_refusee_si_doublon(self):
        donnees = {"nom": "Doublon", "pokemon1": 1, "pokemon2": 1,
                   "pokemon3": 3, "pokemon4": 4, "pokemon5": 5}
        reponse = self.client.post(reverse("equipes"), donnees)
        self.assertContains(reponse, "5 Pokémon différents")
        self.assertFalse(Equipe.objects.exists())
