from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Testimonial



class TestimonialListView(LoginRequiredMixin, ListView):
    model = Testimonial
    template_name = 'testimonial/testimonial_list.html'
    context_object_name = 'testimonials'
    
class TestimonialDetailView(LoginRequiredMixin, DetailView):
    model = Testimonial
    template_name = 'testimonial/testimonial_detail.html'
    context_object_name = 'testimonialDetailView'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get a list of data entries for the given model
        context['related_entries'] = Testimonial.objects.all().order_by('-created_at')[:5]
        # increment view_count field by 1 every time the DetailView is accessed
        self.object.view_count += 1
        self.object.save()
        return context
    
class TestimonialCreateView(LoginRequiredMixin, CreateView):
    model = Testimonial
    template_name = 'testimonial/testimonial_form.html'
    fields = ['title', 'image', 'video_url', 'description']
    success_url = reverse_lazy('testimonial:testimonial_list')
    extra_context = {'is_create': True}
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class TestimonialUpdateView(LoginRequiredMixin, UpdateView):
    model = Testimonial
    template_name = 'testimonial/testimonial_form.html'
    fields = ['title', 'image', 'video_url', 'description']
    success_url = reverse_lazy('testimonial:testimonial_list')
    extra_context = {'is_create': False}


class TestimonialDeleteView(LoginRequiredMixin, DeleteView):
    model = Testimonial
    template_name = 'testimonial/testimonial_confirm_delete.html'
    success_url = reverse_lazy('testimonial:testimonial_list')


