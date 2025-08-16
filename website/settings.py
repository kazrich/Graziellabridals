from pathlib import Path
import os
import dj_database_url  # Make sure this is installed

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------
# 🔐 Security
# --------------------------------------------------

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-h2eus7w^sdufy2r4k=jun2b6m_i&w^*ajc08mxb_w!&=c78mm+')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['*']  # You can restrict this later

# --------------------------------------------------
# 🧩 Installed Apps
# --------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graziella',
    'accounts',
    'django_extensions',
]

# --------------------------------------------------
# 🔐 Authentication
# --------------------------------------------------

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# --------------------------------------------------
# ⚙️ Middleware
# --------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For static file serving
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --------------------------------------------------
# 🌐 URLs & WSGI
# --------------------------------------------------

ROOT_URLCONF = 'website.urls'
WSGI_APPLICATION = 'website.wsgi.application'

# --------------------------------------------------
# 🗄️ Database (PostgreSQL via DATABASE_URL)
# --------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'graziella_db',
        'USER': 'graziella_db_user',
        'PASSWORD': 'uy1OAk4kNghl6sha1pPUcHBEhZpss',
        'HOST': 'dpg-d2g5ft8d1b3ps73etkan0-a.internal.render.com',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}


# --------------------------------------------------
# 🔐 Password Validation
# --------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --------------------------------------------------
# 🌍 Internationalization
# --------------------------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Kampala'
USE_I18N = True
USE_TZ = True

# --------------------------------------------------
# 🖼️ Templates
# --------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'accounts.context_processors.user_profile',  # Custom context processor
            ],
        },
    },
]

# --------------------------------------------------
# 📦 Static & Media Files
# --------------------------------------------------

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'website/static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --------------------------------------------------
# 📧 Email Settings
# --------------------------------------------------

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'graziellab889@gmail.com'
EMAIL_HOST_PASSWORD = 'aets wwjw pydn fvqa'  # App password

# --------------------------------------------------
# 🧠 Default Field Type
# --------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
