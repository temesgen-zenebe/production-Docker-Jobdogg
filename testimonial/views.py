from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Testimonial

class TestimonialListView(ListView):
    model = Testimonial
    context_object_name = 'testimonialList'

class TestimonialDetailView(DetailView):
    model = Testimonial
    context_object_name = 'testimonialDetailView'

class TestimonialCreateView(LoginRequiredMixin, CreateView):
    model = Testimonial
    fields = ['author', 'video_url','description']
    success_url = reverse_lazy('testimonial_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TestimonialUpdateView(LoginRequiredMixin, UpdateView):
    model = Testimonial
    fields = ['author', 'video_url', 'description']
    success_url = reverse_lazy('testimonial_list')

class TestimonialDeleteView(LoginRequiredMixin, DeleteView):
    model = Testimonial
    success_url = reverse_lazy('testimonial_list')
