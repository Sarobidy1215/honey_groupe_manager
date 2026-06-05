from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from .models import ResultatCotation
from django.shortcuts import render
import os
from django.conf import settings
from reportlab.lib.utils import ImageReader


def index(request):
    return render(request, 'index.html')


@login_required
def generer_pdf_devis(request, resultat_id):
    # 1. Récupération des données
    resultat = get_object_or_404(ResultatCotation, id=resultat_id)
    demande = resultat.demande
    circuit = demande.circuit

    # 2. Préparation de la réponse HTTP
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = (
        f'attachment; filename="Devis_HoneyGroup_{demande.id}.pdf"'
    )

    # 3. Création du PDF avec ReportLab
    p = canvas.Canvas(response, pagesize=A4)

    largeur, hauteur = A4

    # =========================
    # LOGO HONEY GROUP
    # =========================

    logo_path = os.path.join(
        settings.BASE_DIR,
        'cotation',
        'static',
        'img',
        'honey.jpg'
    )

    if os.path.exists(logo_path):
        p.drawImage(
            ImageReader(logo_path),
            50,
            hauteur - 100,
            width=80,
            height=80,
            mask='auto'
        )

    # --- EN-TÊTE ---
    p.setFont("Helvetica-Bold", 16)

    p.drawString(
        150,
        hauteur - 50,
        "HONEY GROUP MADAGASCAR"
    )

    p.setFont("Helvetica", 10)

    p.drawString(
        150,
        hauteur - 65,
        "Expert en prestations touristiques"
    )

    p.drawString(
        150,
        hauteur - 80,
        f"Date du devis : {resultat.date_calcul.strftime('%d/%m/%Y %H:%M')}"
    )

    # --- INFORMATIONS CLIENT / CIRCUIT ---
    p.setFont("Helvetica-Bold", 12)

    p.drawString(
        50,
        hauteur - 120,
        "DÉTAILS DE LA COTATION"
    )

    p.line(50, hauteur - 125, 550, hauteur - 125)

    p.setFont("Helvetica", 11)

    p.drawString(
        50,
        hauteur - 145,
        f"Référence : COT-{demande.id}"
    )

    p.drawString(
        50,
        hauteur - 160,
        f"Agent responsable : {demande.auteur}"
    )

    p.drawString(
        50,
        hauteur - 175,
        f"Circuit : {circuit.nom_circuit if circuit else 'N/A'}"
    )

    p.drawString(
        50,
        hauteur - 190,
        f"Nombre de voyageurs (PAX) : {demande.nb_pax}"
    )

    p.drawString(
        50,
        hauteur - 205,
        f"Véhicule prévu : {demande.type_vehicule}"
    )

    # --- TABLEAU DES RÉSULTATS ---
    # Fond gris pour le titre
    p.setFillColor(colors.lightgrey)

    p.rect(
        50,
        hauteur - 260,
        500,
        25,
        fill=1
    )

    p.setFillColor(colors.black)

    p.setFont("Helvetica-Bold", 12)

    p.drawString(
        60,
        hauteur - 253,
        "DÉSIGNATION"
    )

    p.drawString(
        400,
        hauteur - 253,
        "MONTANT"
    )

    p.setFont("Helvetica", 11)

    # Prix en Ar
    p.drawString(
        60,
        hauteur - 285,
        "Total Prestations et Transport (MGA)"
    )

    p.drawRightString(
        540,
        hauteur - 285,
        f"{resultat.prix_vente:,.2f} Ar".replace(',', ' ')
    )

    # Prix en Euro
    p.setFont("Helvetica-Bold", 11)

    p.drawString(
        60,
        hauteur - 310,
        "TOTAL NET À PAYER (EURO)"
    )

    p.drawRightString(
        540,
        hauteur - 310,
        f"{resultat.prix_vente_euro:,.2f} €"
    )

    # Taux de change
    p.setFont("Helvetica-Oblique", 9)

    p.drawString(
        60,
        hauteur - 330,
        f"* Taux de change appliqué : 1 € = {resultat.taux_echange} MGA"
    )

    # --- PIED DE PAGE ---
    p.setFont("Helvetica", 8)

    p.line(50, 50, 550, 50)

    p.drawCentredString(
        largeur / 2,
        40,
        "Honey Group Madagascar - Document généré dynamiquement par le Module de Cotation Django."
    )

    # 4. Finalisation
    p.showPage()
    p.save()

    return response