from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from cotation.views import index, generer_pdf_devis
from django.contrib.auth import get_user_model

urlpatterns = [
    path('', index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('admin/', admin.site.urls),
    path('devis-pdf/<int:resultat_id>/', generer_pdf_devis, name='generer_pdf_devis'),
]

# --- SCRIPT AUTOMATIQUE POUR RENDER ---
# Ce code crée l'admin si la base SQLite est vide [cite: 34, 36]
try:
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            "admin", 
            "admin@admin.com", 
            "honey1205"
        )
        print("Superutilisateur créé avec succès !")
except Exception as e:
    # On utilise un try/except pour éviter que le site plante si la base n'est pas encore migrée
    print(f"Erreur lors de la création de l'admin : {e}")