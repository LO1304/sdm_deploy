from django.contrib import admin
from .models import Khassida,Coran,Zikr,Wird,ContenuDuJour,ParametresPriere,HistoriqueZikr,Son,Profile






# Register your models here.
admin.site.register(Khassida)
admin.site.register(Coran)
admin.site.register(Zikr)
admin.site.register(Wird)
admin.site.register(ContenuDuJour)
admin.site.register(ParametresPriere)
admin.site.register(HistoriqueZikr)
admin.site.register(Profile)
@admin.register(Son)





class KhassidaAdmin(admin.ModelAdmin):
    search_fields = ['titre', 'auteur'] # Cela crée une barre de recherche en haut


class SonAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'date_ajout')
    list_filter = ('categorie',)
    search_fields = ('titre',)


