from django.urls import path
from .views import TestimonialListView, TestimonialDetailView, TestimonialCreateView, TestimonialUpdateView, TestimonialDeleteView

app_name = 'testimonial'

urlpatterns = [
    path('testimonial-list', TestimonialListView.as_view(), name='testimonial_list'),
    path('<int:pk>/', TestimonialDetailView.as_view(), name='testimonial_detail'),
    path('create/', TestimonialCreateView.as_view(), name='testimonial_create'),
    path('<int:pk>/update/', TestimonialUpdateView.as_view(), name='testimonial_update'),
    path('<int:pk>/delete/', TestimonialDeleteView.as_view(), name='testimonial_delete'),
]
