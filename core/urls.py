from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from cotation.views import (
    index,
    generer_pdf_devis,
)

urlpatterns = [

    # =========================
    # PAGE D'ACCUEIL
    # =========================
    path('', index, name='index'),

    # =========================
    # LOGIN
    # =========================
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html'
        ),
        name='login'
    ),

    # =========================
    # ADMIN
    # =========================
    path('admin/', admin.site.urls),

    # =========================
    # PDF
    # =========================
    path(
        'devis-pdf/<int:resultat_id>/',
        generer_pdf_devis,
        name='generer_pdf_devis'
    ),

]