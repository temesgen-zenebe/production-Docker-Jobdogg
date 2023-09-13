from django.urls import path
from . import views

app_name = 'timeCard'

urlpatterns = [
    path('time-card/time-card-management/', views.TimeCardManagement.as_view(), name='time-card-management'),
    path('time-card/timecards/', views.TimeCardListView.as_view(), name='timecard_list'),
    path('time-card/timecards/<slug:slug>/', views.TimeCardDetailView.as_view(), name='timecard_detail'),
    path('time-card/create_time_assigned/', views.create_time_assigned, name='create_time_assigned'),
    path('time-card/create_date_assigned/', views.create_date_assigned, name='create_date_assigned'),
    path('time-card/create_time_card/', views.create_time_card, name='create_time_card'),
   
]