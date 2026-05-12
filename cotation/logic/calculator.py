import math

class CotationCalculator:
    def __init__(self, demande):
        self.demande = demande
        self.circuit = demande.circuit
        from ..models import ParametreGlobal
        self.params = {p.cle: float(p.valeur) for p in ParametreGlobal.objects.all()}

    def get_param(self, key, default=0):
        return self.params.get(key, default)

    def calculer_transport(self):
        dist = self.circuit.distance_aller_km
        conso = self.demande.conso_vehicule
        prix_l = self.get_param('PRIX_CARBURANT', 5000)
        return (dist * 2 * conso * prix_l) / 100

    def calculer_prestations(self):
        total = 0
        nb_pax = self.demande.nb_pax
        nb_chambres = math.ceil(nb_pax / 2)
        
        for jour in self.circuit.jours.all():
            for ligne in jour.prestations.all():
                if not ligne.tarif_reference: continue
                prix_u = ligne.tarif_reference.base_prix
                
                u = ligne.unite.upper()
                if u == "PAX": total += prix_u * nb_pax
                elif u == "NUIT": total += prix_u * nb_chambres
                elif u == "JOUR": total += prix_u * 1
                else: total += prix_u * ligne.quantite_par_defaut
        return total

    def generer_devis_final(self):
        transport = self.calculer_transport()
        prestations = self.calculer_prestations()
        cout_revient = transport + prestations
        marge = self.get_param('MARGE_AGENCE', 0.15)
        prix_vente_mga = cout_revient * (1 + marge)
        taux = self.get_param('TAUX_EURO', 5000)
        
        return {
            'cout_revient': cout_revient,
            'prix_vente_mga': prix_vente_mga,
            'prix_vente_eur': prix_vente_mga / taux if taux > 0 else 0,
            'taux_applique': taux
        }