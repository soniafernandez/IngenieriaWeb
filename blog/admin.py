from django.contrib import admin
from .models import Receta, Alimento, Ingredientes

# Register your models here.
admin.site.register(Receta)
admin.site.register(Ingredientes)
admin.site.register(Alimento)