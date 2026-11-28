"""Adresses (URL) du site et la vue Django qui répond à chacune."""
from django.contrib import admin
from django.urls import path

from pokédex.views import detail, equipes, home, supprimer_equipe
from pokédex.views_combat import combat

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('pokemon/<int:pokemon_id>/', detail, name='detail'),
    path('equipes/', equipes, name='equipes'),
    path('equipes/<int:equipe_id>/supprimer/', supprimer_equipe, name='supprimer_equipe'),
    path('combat/', combat, name='combat'),
]
