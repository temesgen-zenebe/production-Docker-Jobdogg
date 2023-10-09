import os
from pathlib import Path
from decouple import config
import dj_database_url
import paypalrestsdk
import stripe

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Debug mode
DEBUG = True

# Allowed Hosts
ALLOWED_HOSTS = [
    'jobdogg-com.up.railway.app',  # Add your production domain/host here
    '127.0.0.1',  # Add your local development server IP or hostname here
]

# Secret Key and SendGrid API Key
SECRET_KEY = config('SECRET_KEY')
SENDGRID_API_KEY = config('SENDGRID_API_KEY')

# Installed Apps
INSTALLED_APPS = [
    # Built-in Django apps
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    # Third-party
    'crispy_forms',
    'crispy_bootstrap5',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'corsheaders',
    
    # Local apps
    'common.apps.CommonConfig',
    'users.apps.UsersConfig',
    'pages.apps.PagesConfig', 
    'testimonial.apps.TestimonialConfig', 
    'employee.apps.EmployeeConfig', 
    'employer.apps.EmployerConfig', 
    'supperAdmin.apps.SupperadminConfig', 
    'subscription.apps.SubscriptionConfig',
    'recommendedByAI.apps.RecommendedbyaiConfig',
    'JobFilter.apps.JobfilterConfig',
    'timeCard.apps.TimecardConfig',
]

SITE_ID = 1

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


CSRF_TRUSTED_ORIGINS = ['https://jobdogg-com.up.railway.app', 'http://127.0.0.1:8000']


if not DEBUG:
    CSRF_TRUSTED_ORIGINS = ['https://jobdogg-com.up.railway.app']


# CORS Allowed Origins
if DEBUG:
    CORS_ALLOWED_ORIGINS = ['http://127.0.0.1:8000']
    
# Enforce secure session cookies (only send over HTTPS)
SESSION_COOKIE_SECURE = True

# Enforce secure CSRF cookies (only send over HTTPS)
CSRF_COOKIE_SECURE = True

# Define the view or URL to handle CSRF failure errors
#CSRF_FAILURE_VIEW = 'common.views.csrf_failure_view'  # Replace 'yourapp.views.csrf_failure_view' with the actual view or URL you want to use.


# Root URL Configuration
ROOT_URLCONF = 'jobDoggApp.urls'

# Templates Configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
         'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI Application
WSGI_APPLICATION = 'jobDoggApp.wsgi.application'

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'RMwtxRrgpU3mtY34oT8e',
        'HOST': 'containers-us-west-191.railway.app',
        'PORT': 8067
    }
}

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
DEFAULT_FROM_EMAIL = 'temf2006@gmail.com'

# Authentication Settings
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, even w/o `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth`-specific auth methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Additional Authentication Settings
ACCOUNT_SIGNUP_FORM_CLASS = 'users.forms.SignupForm'
LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'pages:redirect_to_homepage'

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Custom User Model
AUTH_USER_MODEL = 'users.CustomUser'

# Internationalization Settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
# # Local Static File Settings


STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Add the following line at the end of the settings.py file
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

ALLOWED_VIDEO_EXTENSIONS = ['.mp4', '.mpg', '.avi', '.mov', '.mkv', '.wmv', '.ogv', '.webm', '.flv']
MAX_VIDEO_DURATION = 60  # 1 minutes in seconds

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

