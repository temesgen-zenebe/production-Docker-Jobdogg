from django.urls import path
from . import views

app_name = 'timeCard'

urlpatterns = [
    path('timecards/', views.TimeCardListView.as_view(), name='timecard_list'),
    path('timecards/<slug:slug>/', views.TimeCardDetailView.as_view(), name='timecard_detail'),
    path('create_time_assigned/', views.create_time_assigned, name='create_time_assigned'),
    path('create_date_assigned/', views.create_date_assigned, name='create_date_assigned'),
    path('create_time_card/', views.create_time_card, name='create_time_card'),
   
]