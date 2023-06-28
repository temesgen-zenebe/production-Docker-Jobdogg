from django.urls import path
from .views import (AboutUsView, HomePageView ,ContactUsView, OurDoggsView, GetStaffView, GetWorkView)
from . import views

app_name = 'pages' 

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about-us/', AboutUsView.as_view(), name='about-us'),
    path('contact-us/', ContactUsView.as_view(), name='contact-us'),
    path('Our-Dogs/', OurDoggsView.as_view(), name='gurDoggsView'),
    path('get-Staff/', GetStaffView.as_view(), name='getStaffView'),
    path('get-Work/', GetWorkView.as_view(), name='getWorkView'),
]