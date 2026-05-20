# Fleeting Logistics App - Render Deployment Notes

## Summary
Django logistics app deployed on Render with PostgreSQL database.

## Current State (May 2026)
- **URL**: https://fleeting.onrender.com
- **Database**: PostgreSQL at dpg-d85jd6gg4nts7382nnm0-a/fleeting
- **Admin Credentials**: admin / admin123

## Issues Fixed

### 1. Database Connection
- Originally tried SQLite fallback
- Final config: Uses PostgreSQL when DATABASE_URL is set
- Settings parses `os.environ.get('DATABASE_URL')` with dj-database-url

### 2. wsgi.py - Database Check Bug
- **Problem**: Code checked `sqlite_master` (SQLite) instead of PostgreSQL
- **Fix**: Run migrations and create admin on every startup

```python
# Run migrations automatically on startup
try:
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
except Exception as e:
    print(f"Migration error: {e}")

# Create admin user on startup
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@fleeting.com', 'admin123')
except Exception as e:
    print(f"Admin creation error: {e}")
```

### 3. Static Files
- **Problem**: Wrong path operator (`BASE_DIR / 'staticfiles'` vs `os.path.join()`)
- **Fix**: Use explicit `os.path.join()`:

```python
import os
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 4. render.yaml Configuration
```yaml
buildCommand: |
  export DATABASE_URL="postgres://default:mbIjZTsEtRvnm569hArA2CSW0WN5TjGE@dpg-d85jd6gg4nts7382nnm0-a/fleeting"
  python -m pip install -r requirements.txt
  python manage.py migrate --no-input
  python manage.py collectstatic --no-input
```

## URLs
- Home: /
- Dashboard: /dashboard/ (requires login)
- Admin: /admin/
- Admin Bookings: /admin/logistics/booking/

## Dependencies
- Django==4.2.30
- dj-database-url
- whitenoise
- gunicorn
- psycopg-binary
- python-dotenv
- pillow

## Common Issues
1. If 500 error on dashboard - check Render logs for migration errors
2. If static files 404 - redeploy to trigger collectstatic
3. If login fails - worker will auto-create admin on restart