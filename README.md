# Pokelatte backend

Django REST API for Pokelatte.

## Local development

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Local development uses `db.sqlite3`. Production uses the database configured by
`DATABASE_URL`.

## Free deployment: Render + Neon

[Render](https://render.com/) hosts the web service. Its free services sleep
after 15 minutes without traffic, so the first request can take about a minute.
[Neon](https://neon.com/) provides persistent Postgres storage on its permanent
free tier.

1. Create a free Neon project and copy its **pooled connection string**.
2. In Render, choose **New > Blueprint**, connect this GitHub repository, and
   apply `render.yaml`.
3. When Render prompts for `DATABASE_URL`, paste the Neon connection string.
4. After the deployment succeeds, use the generated `.onrender.com` URL as the
   frontend API URL.

Render generates `SECRET_KEY`, disables debug mode, applies migrations, and
collects static files during every deployment.

### Move the existing SQLite data

Do not commit the generated backup because it contains user data.

```powershell
python -X utf8 manage.py dumpdata --natural-foreign --natural-primary --exclude contenttypes --exclude auth.permission --indent 2 -o backup.json
$env:DATABASE_URL = "<your Neon pooled connection string>"
python manage.py migrate
python manage.py loaddata backup.json
Remove-Item Env:DATABASE_URL
Remove-Item backup.json
```

### Environment variables

To use different frontend or custom domains, update these values in Render:

| Variable | Value |
| --- | --- |
| `ALLOWED_HOSTS` | Comma-separated API custom domains, without schemes |
| `CORS_ALLOWED_ORIGINS` | Comma-separated frontend origins, including `https://` |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated trusted origins, including `https://` |
