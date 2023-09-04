# myapp/urls.py (or your project's main urls.py)

from django.urls import path
from . import views

app_name = 'common' 

urlpatterns = [
    # ... other URL patterns ...

    # Define the URL pattern for CSRF failure
    path('csrf_failure/', views.csrf_failure_view, name='csrf_failure'),

    # ... other URL patterns ...
]
