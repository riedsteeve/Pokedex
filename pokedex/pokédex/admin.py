from django.contrib import admin

# Register your models here.

from .models import Equipe, Pokemon

admin.site.register(Pokemon)
admin.site.register(Equipe)
