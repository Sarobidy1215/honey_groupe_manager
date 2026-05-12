from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    CatalogueDestination,
    ReferenceTarifaire,
    Circuit,
    CircuitJour,
    LignePrestation,
    DemandeCotation,
    ResultatCotation,
    ParametreGlobal
)

# --- HEADER ADMIN ---
admin.site.site_header = mark_safe(
    '<img src="/static/img/honey.jpg" style="height: 40px; vertical-align: middle; margin-right: 10px;">'
    '<span style="color: #004a99;">HONEY GROUP - Gestion des Cotations</span>'
)
admin.site.site_title = "Honey Group Admin"
admin.site.index_title = "Tableau de Bord des Experts"


# --- BASE ADMIN STYLE ---
class HoneyStyleAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('css/honey_admin.css',)
        }


# --- INLINE (DÉSACTIVÉ TEMPORAIREMENT POUR ÉVITER 500) ---
class ReferenceTarifaireInline(admin.TabularInline):
    model = ReferenceTarifaire
    extra = 1


class LignePrestationInline(admin.TabularInline):
    model = LignePrestation
    extra = 2


# --- DESTINATION ---
@admin.register(CatalogueDestination)
class CatalogueDestinationAdmin(HoneyStyleAdmin):
    list_display = ('nom_destination', 'get_nb_tarifs')
    search_fields = ('nom_destination',)
    inlines = [ReferenceTarifaireInline]

    def get_nb_tarifs(self, obj):
        return obj.tarifs.count()


# --- TARIF ---
@admin.register(ReferenceTarifaire)
class ReferenceTarifaireAdmin(HoneyStyleAdmin):
    list_display = ('libelle', 'destination', 'type_prestation', 'base_prix', 'devise', 'actif')
    list_filter = ('destination', 'type_prestation', 'actif')
    search_fields = ('libelle', 'destination__nom_destination')
    list_editable = ('base_prix', 'actif')


# --- CIRCUIT JOUR (INLINE DÉSACTIVÉ POUR STABILITÉ) ---
@admin.register(CircuitJour)
class CircuitJourAdmin(HoneyStyleAdmin):
    list_display = ('circuit', 'numero_jour')
    list_filter = ('circuit',)
    # inlines = [LignePrestationInline]  # TEMPORAIREMENT OFF


# --- CIRCUIT ---
@admin.register(Circuit)
class CircuitAdmin(HoneyStyleAdmin):
    list_display = ('nom_circuit', 'duree', 'distance_aller_km')


# --- DEMANDE ---
@admin.register(DemandeCotation)
class DemandeCotationAdmin(HoneyStyleAdmin):
    list_display = ('id', 'circuit', 'nb_pax', 'auteur', 'date_depart')
    list_filter = ('circuit', 'date_depart')
    search_fields = ('auteur', 'id')


# --- RESULTAT ---
@admin.register(ResultatCotation)
class ResultatCotationAdmin(HoneyStyleAdmin):

    list_display = ('demande', 'get_prix_mga', 'get_prix_eur', 'pdf_link')

    readonly_fields = (
        'demande',
        'cout_total',
        'prix_vente',
        'prix_vente_euro',
        'taux_echange'
    )

    def get_prix_mga(self, obj):
        if not obj or not obj.prix_vente:
            return "0 Ar"
        return f"{obj.prix_vente:,.2f} Ar".replace(',', ' ')

    get_prix_mga.short_description = "Prix (MGA)"

    def get_prix_eur(self, obj):
        if not obj or not obj.prix_vente_euro:
            return "0 €"
        return f"{obj.prix_vente_euro:,.2f} €"

    get_prix_eur.short_description = "Prix (€)"

    def pdf_link(self, obj):
        try:
            url = reverse('generer_pdf_devis', args=[obj.id])
            return mark_safe(f'''
                <a class="button" href="{url}" target="_blank"
                   style="background-color:#f37021;color:white;padding:5px 15px;
                   border-radius:20px;text-decoration:none;font-weight:bold;">
                   📄 EXPORTER PDF
                </a>
            ''')
        except:
            return "PDF indisponible"

    pdf_link.short_description = "Action"


# --- PARAMETRE GLOBAL ---
@admin.register(ParametreGlobal)
class ParametreGlobalAdmin(HoneyStyleAdmin):
    list_display = ('cle', 'valeur', 'description')
    list_editable = ('valeur',)