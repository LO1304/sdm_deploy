from django.contrib import admin
from .models import Khassida, Coran, Zikr, Wird, ContenuDuJour, ParametresPriere, HistoriqueZikr, Son, Profile

class KhassidaAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur')
    search_fields = ['titre', 'auteur']

class SonAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'date_ajout')
    list_filter = ('categorie',)
    search_fields = ('titre',)

# Register your models here.
admin.site.register(Khassida, KhassidaAdmin)
admin.site.register(Coran)
admin.site.register(Zikr)
admin.site.register(Wird)
admin.site.register(ContenuDuJour)
admin.site.register(ParametresPriere)
admin.site.register(HistoriqueZikr)
admin.site.register(Profile)
admin.site.register(Son, SonAdmin)
