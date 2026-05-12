from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# --- 1. PARAMETRES GLOBAUX ---
class ParametreGlobal(models.Model):
    cle = models.CharField(max_length=100, unique=True, verbose_name="Clé")
    valeur = models.FloatField(verbose_name="Valeur")
    type_donnee = models.CharField(max_length=50, help_text="ex: decimal, entier")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Paramètre Global"
        verbose_name_plural = "Paramètres Globaux"

    def __str__(self):
        return self.cle

# --- 2. CATALOGUE DES TARIFS ---
class CatalogueDestination(models.Model):
    nom_destination = models.CharField(max_length=100, unique=True, verbose_name="Destination")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Destination"

    def __str__(self):
        return self.nom_destination

class ReferenceTarifaire(models.Model):
    destination = models.ForeignKey(CatalogueDestination, on_delete=models.CASCADE, related_name="tarifs")
    libelle = models.CharField(max_length=255, verbose_name="Libellé")
    type_prestation = models.CharField(max_length=100, help_text="HOTEL, RESTO, VISITE, TRANSPORT")
    base_prix = models.FloatField(verbose_name="Prix de base")
    devise = models.CharField(max_length=10, default="MGA")
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Référence Tarifaire"

    def __str__(self):
        return f"{self.libelle} ({self.base_prix} {self.devise})"

# --- 3. CIRCUITS ---
class Circuit(models.Model):
    nom_circuit = models.CharField(max_length=255, verbose_name="Nom du Circuit")
    duree = models.IntegerField(help_text="Nombre de jours")
    distance_aller_km = models.FloatField(default=0, help_text="Distance simple aller")
    
    def __str__(self):
        return self.nom_circuit

class CircuitJour(models.Model):
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE, related_name="jours")
    numero_jour = models.IntegerField(verbose_name="Jour n°")
    description_jour = models.TextField()

    def __str__(self):
        return f"{self.circuit.nom_circuit} - Jour {self.numero_jour}"

class LignePrestation(models.Model):
    circuit_jour = models.ForeignKey(CircuitJour, on_delete=models.CASCADE, related_name="prestations")
    tarif_reference = models.ForeignKey(ReferenceTarifaire, on_delete=models.CASCADE, null=True, verbose_name="Prestation")
    quantite_par_defaut = models.FloatField(default=1)
    unite = models.CharField(max_length=50, help_text="PAX, NUIT, JOUR, FORFAIT")

# --- 4. COTATIONS (RESULTATS) ---
class DemandeCotation(models.Model):
    circuit = models.ForeignKey(Circuit, on_delete=models.SET_NULL, null=True)
    nb_pax = models.IntegerField(verbose_name="Nombre de personnes")
    date_depart = models.DateField()
    type_vehicule = models.CharField(max_length=100)
    conso_vehicule = models.FloatField(default=15, help_text="L/100km")
    auteur = models.CharField(max_length=100, verbose_name="Établi par")

    class Meta:
        verbose_name = "Demande de Cotation"

    def __str__(self):
        return f"Cotation #{self.id} - {self.circuit}"

class ResultatCotation(models.Model):
    demande = models.OneToOneField(DemandeCotation, on_delete=models.CASCADE)
    cout_total = models.FloatField(verbose_name="Coût de revient")
    prix_vente = models.FloatField(verbose_name="Prix de vente (MGA)")
    prix_vente_euro = models.FloatField(verbose_name="Prix de vente (€)")
    taux_echange = models.FloatField(verbose_name="Taux utilisé")
    date_calcul = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Résultat de la Cotation"

# --- SIGNAL DE CALCUL AUTOMATIQUE ---
 @receiver(post_save, sender=DemandeCotation)
def auto_calculer(sender, instance, created, **kwargs):
    try:
        # 🔒 sécurité : si pas de circuit → on stop
        if not instance.circuit:
            return

        from .logic.calculator import CotationCalculator

        calc = CotationCalculator(instance)
        res = calc.generer_devis_final()

        ResultatCotation.objects.update_or_create(
            demande=instance,
            defaults={
                'cout_total': res['cout_revient'],
                'prix_vente': res['prix_vente_mga'],
                'prix_vente_euro': res['prix_vente_eur'],
                'taux_echange': res['taux_applique'],
            }
        )

    except Exception as e:
        # 🔒 empêche le crash de l’admin
        print("Erreur calcul cotation:", e)