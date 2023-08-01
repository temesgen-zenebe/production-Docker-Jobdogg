from django.urls import path
from .views import (AboutUsView, HomePageView ,ContactUsView, OurDoggsView, GetStaffView, GetWorkView)
from . import views

app_name = 'pages' 

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('pages/', views.redirect_to_homepage, name='redirect_to_homepage'),  # This is the correct URL pattern
    path('pages/employee/', views.employee_home, name='employeeHomePage'),
    path('pages/employer/', views.employer_home, name='employerHomePage'),
    path('pages/admin/', views.admin_home, name='adminHomePage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about-us/', AboutUsView.as_view(), name='about-us'),
    path('contact-us/', ContactUsView.as_view(), name='contact-us'),
    path('Our-Dogs/', OurDoggsView.as_view(), name='gurDoggsView'),
    path('get-Staff/', GetStaffView.as_view(), name='getStaffView'),
    path('get-Work/', GetWorkView.as_view(), name='getWorkView'),
]