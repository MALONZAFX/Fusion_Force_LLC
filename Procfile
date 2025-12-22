# Create Procfile
@'
web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn fusion_force.wsgi:application --bind 0.0.0.0:$PORT
'@ | Out-File -FilePath "Procfile" -Encoding UTF8