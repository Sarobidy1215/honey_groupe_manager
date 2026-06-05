from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.urls import reverse


# =========================
# INLINE PRESTATIONS
# =========================

class LignePrestationInline(admin.TabularInline):
    model = LignePrestation
    extra = 1


# =========================
# ENREGISTREMENTS ADMIN
# =========================

@admin.register(ParametreGlobal)
class ParametreGlobalAdmin(admin.ModelAdmin):
    list_display = ('cle', 'valeur')


@admin.register(CatalogueDestination)
class CatalogueDestinationAdmin(admin.ModelAdmin):
    list_display = ('nom_destination',)


@admin.register(ReferenceTarifaire)
class ReferenceTarifaireAdmin(admin.ModelAdmin):
    list_display = (
        'libelle',
        'destination',
        'type_prestation',
        'base_prix',
        'devise'
    )


@admin.register(Circuit)
class CircuitAdmin(admin.ModelAdmin):
    list_display = ('nom_circuit', 'duree')


@admin.register(CircuitJour)
class CircuitJourAdmin(admin.ModelAdmin):
    list_display = ('circuit', 'numero_jour')

    # IMPORTANT
    inlines = [LignePrestationInline]


@admin.register(DemandeCotation)
class DemandeCotationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'circuit',
        'nb_pax',
        'date_depart',
        'auteur'
    )


@admin.register(ResultatCotation)
class ResultatCotationAdmin(admin.ModelAdmin):
    list_display = (
        'demande',
        'cout_total',
        'prix_vente',
        'prix_vente_euro',
        'export_pdf'
    )

    def export_pdf(self, obj):
        url = reverse('generer_pdf_devis', args=[obj.id])

        return format_html(
            '<a class="button" href="{}" target="_blank">📄 Générer PDF</a>',
            url
        )

    export_pdf.short_description = "PDF"


# LignePrestation déjà gérée INLINE
# donc inutile de la register séparément