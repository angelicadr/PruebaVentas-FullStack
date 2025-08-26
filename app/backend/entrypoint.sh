#!/usr/bin/env bash
set -e

# Wait for Postgres
echo "Waiting for db $POSTGRES_HOST:$POSTGRES_PORT..."
until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done
echo "DB is up!"

python manage.py collectstatic --noinput || true
python manage.py migrate --noinput
python manage.py loaddata seeds.json || true

# Create superuser if not exists
python - <<'PY'
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE","config.settings")
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
u = os.environ.get("DJANGO_SUPERUSER_USERNAME","admin")
if not User.objects.filter(username=u).exists():
    User.objects.create_superuser(u, os.environ.get("DJANGO_SUPERUSER_EMAIL","admin@example.com"), os.environ.get("DJANGO_SUPERUSER_PASSWORD","admin"))
    print("Superuser created")
else:
    print("Superuser exists")
PY

python manage.py runserver 0.0.0.0:8000
