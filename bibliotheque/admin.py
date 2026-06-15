from django.contrib import admin
from .models import Khassida, Coran, Zikr, Wird, ContenuDuJour, ParametresPriere, HistoriqueZikr, Son, Profile

class KhassidaAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur')
    search_fields = ['titre', 'auteur']

class SonAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'date_ajout')
    list_filter = ('categorie',)
    search_fields = ('titre',)

class ContenuDuJourAdmin(admin.ModelAdmin):
    list_display = ('date', 'apercu_verset', 'apercu_rappel')
    search_fields = ('verset_du_jour', 'rappel_dujour')
    ordering = ('-date',)
    
    def apercu_verset(self, obj):
        return obj.verset_du_jour[:50] + '...' if obj.verset_du_jour and len(obj.verset_du_jour) > 50 else obj.verset_du_jour
    apercu_verset.short_description = "Verset"
    
    def apercu_rappel(self, obj):
        return obj.rappel_dujour[:50] + '...' if obj.rappel_dujour and len(obj.rappel_dujour) > 50 else obj.rappel_dujour
    apercu_rappel.short_description = "Rappel"

# Register your models here.
admin.site.register(Khassida, KhassidaAdmin)
admin.site.register(Coran)
admin.site.register(Zikr)
admin.site.register(Wird)
admin.site.register(ContenuDuJour, ContenuDuJourAdmin)
admin.site.register(ParametresPriere)
admin.site.register(HistoriqueZikr)
admin.site.register(Profile)
admin.site.register(Son, SonAdmin)
