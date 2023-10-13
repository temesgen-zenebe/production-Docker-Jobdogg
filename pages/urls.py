from django.urls import path
from .views import SubscriberListView, SubscriberCreateView, SubscriberUpdateView, SubscriberDeleteView
from .views import (AboutUsView, HomePageView ,ContactUsView, ExecutiveTeam, BlogView, OurDoggsView, GetStaffView, GetWorkView)
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
    path('executive-team/', ExecutiveTeam.as_view(), name='executive-team'),
    path('blog/', BlogView.as_view(), name='blogPage'),
    path('Our-Dogs/', OurDoggsView.as_view(), name='gurDoggsView'),
    path('get-Staff/', GetStaffView.as_view(), name='getStaffView'),
    path('get-Work/', GetWorkView.as_view(), name='getWorkView'),


    #newsletter'
    path('list/', SubscriberListView.as_view(), name='subscriber_list'),
    path('add/', SubscriberCreateView.as_view(), name='subscriber_create'),
    path('<int:pk>/edit/', SubscriberUpdateView.as_view(), name='subscriber_edit'),
    path('<int:pk>/delete/', SubscriberDeleteView.as_view(), name='subscriber_delete'),
]
