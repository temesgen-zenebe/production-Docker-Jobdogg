# subscription/urls.py
from django.urls import path
from .views import UserDashboardView, SubscriptionCreateView, PaymentProcessView

app_name = 'subscription'
urlpatterns = [
    path('subscription/dashboard/', UserDashboardView.as_view(), name='user_dashboard'),
    path('subscription/create-subscription/', SubscriptionCreateView.as_view(), name='subscription_create'),
    path('subscription/process-payment/<slug:slug>/', PaymentProcessView.as_view(), name='payment_process'),
    # Add more URLs as needed
]
