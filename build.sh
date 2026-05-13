#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Crée le superutilisateur de manière sécurisée si la variable est présente
if [ "$CREATE_ADMIN" = "true" ]; then
    python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() || User.objects.create_superuser('admin', 'admin@admin.com', 'honey1205')"
fi