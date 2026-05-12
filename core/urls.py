from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from cotation.views import index, generer_pdf_devis

urlpatterns = [
    path('', index, name='index'),

    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    path('admin/', admin.site.urls),

    path('devis-pdf/<int:resultat_id>/', generer_pdf_devis, name='generer_pdf_devis'),
]