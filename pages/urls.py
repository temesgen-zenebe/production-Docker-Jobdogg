from django.urls import path

from .views import AboutUsView, HomePageView ,ContactUsView

app_name = 'pages'

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('about-us/', AboutUsView.as_view(), name='about-us'),
    path('contact-us/', ContactUsView.as_view(), name='contact-us'),
]