from django.contrib import admin
from .models import *

admin.site.register(ParametreGlobal)
admin.site.register(CatalogueDestination)
admin.site.register(ReferenceTarifaire)
admin.site.register(Circuit)
admin.site.register(CircuitJour)
admin.site.register(LignePrestation)
admin.site.register(DemandeCotation)
admin.site.register(ResultatCotation)