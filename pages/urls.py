from django.urls import path
from .views import SubscriberListView, SubscriberCreateView, SubscriberUpdateView, SubscriberDeleteView
from .views import (AboutUsView, HomePageView ,ContactUsView, ExecutiveTeam,HowItWoksForEmployee,
                    TermsAndPolicy,HowItWoksForEmployer, EmployeeFAQ, EmployerFAQ, BlogView, OurDoggsView, GetStaffView, GetWorkView)
from . import views

app_name = 'pages' 

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('pages/', views.redirect_to_homepage, name='redirect_to_homepage'),  
    path('pages/employee/', views.employee_home, name='employeeHomePage'),
    path('pages/employer/', views.employer_home, name='employerHomePage'),
    path('pages/admin/', views.admin_home, name='adminHomePage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about-us/', AboutUsView.as_view(), name='about-us'),
    path('contact-us/', ContactUsView.as_view(), name='contact-us'),
    path('executive-team/', ExecutiveTeam.as_view(), name='executive-team'),
    path('HowItWoks-ForEmployee/', HowItWoksForEmployee.as_view(), name='HowItWoks-ForEmployee'),
    path('HowItWoks-ForEmployer/', HowItWoksForEmployer.as_view(), name='HowItWoks-ForEmployer'),
    path('employee-FAQ/', EmployeeFAQ.as_view(), name='employeeFAQ'),
    path('employer-FAQ/', EmployerFAQ.as_view(), name='employerFAQ'),
    path('terms-and-Policy-conditions/', TermsAndPolicy.as_view(), name='terms-and-Policy'),
    path('blog/', BlogView.as_view(), name='blogPage'),
    path('Our-Dogs/', OurDoggsView.as_view(), name='ourDoggsView'),
    path('get-Staff/', GetStaffView.as_view(), name='getStaffView'),
    path('get-Work/', GetWorkView.as_view(), name='getWorkView'),


    #newsletter'
    path('list/', SubscriberListView.as_view(), name='subscriber_list'),
    path('add/', SubscriberCreateView.as_view(), name='subscriber_create'),
    path('<int:pk>/edit/', SubscriberUpdateView.as_view(), name='subscriber_edit'),
    path('<int:pk>/delete/', SubscriberDeleteView.as_view(), name='subscriber_delete'),
]
