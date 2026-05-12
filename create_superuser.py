import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ton_projet.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

USERNAME = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
EMAIL = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
PASSWORD = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin12345")

user, created = User.objects.get_or_create(
    username=USERNAME,
    defaults={"email": EMAIL}
)

user.set_password(PASSWORD)
user.is_superuser = True
user.is_staff = True
user.save()

print("Superuser prêt")