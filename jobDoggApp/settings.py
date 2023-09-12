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

# STATIC_URL = 'static/'
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
# Static and Media File Settings
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/'),
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

ALLOWED_VIDEO_EXTENSIONS = ['.mp4', '.mpg', '.avi', '.mov', '.mkv', '.wmv', '.ogv', '.webm', '.flv']
MAX_VIDEO_DURATION = 60  # 1 minutes in seconds

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




# import os
# from pathlib import Path
# import dj_database_url
# from decouple import config
# import paypalrestsdk
# import stripe



# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

# DEBUG = True

# # settings.py

# ALLOWED_HOSTS = [
#     'web-production-d90f.up.railway.app',  # Add your production domain/host here
#     '127.0.0.1',  # Add your local development server IP or hostname here
# ]



# # Quick-start development settings - unsuitable for production

# SECRET_KEY = config('SECRET_KEY')
# SENDGRID_API_KEY =config('SENDGRID_API_KEY')

# INSTALLED_APPS = [
#     # Built-in Django apps
#     'django.contrib.admin',
#     'django.contrib.admindocs',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.sites',
#     'django.contrib.staticfiles',
#     'django.contrib.humanize',
#     'corsheaders',
     
#      # Third-party
#     'crispy_forms',
#     'crispy_bootstrap5',
#     'allauth',
#     'allauth.account',
#     'allauth.socialaccount',
#     'corsheaders',
    
#     #local apps
#     'common.apps.CommonConfig',
#     'users.apps.UsersConfig',
#     'pages.apps.PagesConfig', 
#     'testimonial.apps.TestimonialConfig', 
#     'employee.apps.EmployeeConfig', 
#     'employer.apps.EmployerConfig', 
#     'supperAdmin.apps.SupperadminConfig', 
#     'subscription.apps.SubscriptionConfig',
#     'recommendedByAI.apps.RecommendedbyaiConfig',
#     'JobFilter.apps.JobfilterConfig',
    
# ]
# SITE_ID = 1

# CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

# CRISPY_TEMPLATE_PACK = "bootstrap5"

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# CORS_ALLOWED_ORIGINS = [
#     'http://127.0.0.1:8000',
#     'https://web-production-d90f.up.railway.app',
# ]

# ROOT_URLCONF = 'jobDoggApp.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#          'DIRS': [BASE_DIR/ 'templates'],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'jobDoggApp.wsgi.application'


# # Database
# # https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# """
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }"""


# DATABASES = {
#     'default': {
#     'ENGINE': 'django.db.backends.postgresql',
#     'NAME': 'railway',
#     'USER': 'postgres',
#     'PASSWORD': 'RMwtxRrgpU3mtY34oT8e',
#     'HOST': 'containers-us-west-191.railway.app',
#     'PORT': 8067
#     }
# }

# # EMAIL
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'apikey'
# EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
# DEFAULT_FROM_EMAIL = 'temf2006@gmail.com'


# # # Stripe Configuration
# # stripe.api_key = os.environ.get('STRIPE_API_KEY')

# # # PayPal Configuration
# # paypalrestsdk.configure({
# #     'mode': os.environ.get('PAYPAL_MODE', 'sandbox'),  # Set to 'live' for production environment
# #     'client_id': os.environ.get('PAYPAL_CLIENT_ID'),
# #     'client_secret': os.environ.get('PAYPAL_CLIENT_SECRET'),
# # })

# AUTHENTICATION_BACKENDS = (
# # Needed to login by username in Django admin, even w/o `allauth`
# 'django.contrib.auth.backends.ModelBackend',
# # `allauth`-specific auth methods, such as login by e-mail
# 'allauth.account.auth_backends.AuthenticationBackend',
# )
# ACCOUNT_SIGNUP_FORM_CLASS = 'users.forms.SignupForm'
# # Password validation
# # https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators


# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


# # AUTHENTICATION SETTINGS
# AUTH_USER_MODEL = 'users.CustomUser'
# LOGIN_URL = 'account_login'
# #LOGIN_REDIRECT_URL = 'pages:homepage'
# LOGIN_REDIRECT_URL = 'pages:redirect_to_homepage'


# ## django-allauth settings
# ACCOUNT_AUTHENTICATION_METHOD = 'email' # Default: 'username'
# ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1 # Default: 3
# ACCOUNT_EMAIL_REQUIRED = True # Default: False
# ACCOUNT_EMAIL_VERIFICATION = 'mandatory' # Default: 'optional'
# ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5 # Default: 5
# ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300 # Default 300
# ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login' # Default: '/'
# ACCOUNT_USERNAME_REQUIRED = False # Default: True

# # Internationalization
# # https://docs.djangoproject.com/en/4.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

# USE_I18N = True

# USE_TZ = True


# # Static files (CSS, JavaScript, Images)
# # https://docs.djangoproject.com/en/4.2/howto/static-files/


# STATIC_URL = 'static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]
# MEDIA_URL = 'media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# # Default primary key field type
# # https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field


# ALLOWED_VIDEO_EXTENSIONS = ['.mp4', '.mpg', '.avi', '.mov', '.mkv', '.wmv', '.ogv', '.webm', '.flv']
# MAX_VIDEO_DURATION = 60  # 1 minutes in seconds


# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# # BOTTOM OF settings.py

# # if os.environ.get('ENVIRONMENT') != 'production':
# #     from .local_settings import *
# # # DON'T PUT ANYTHING BELOW THIS
# # The following lines are correct for production deployment on Railway
