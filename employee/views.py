from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, FormView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Policies, UserAcceptedPolicies
from django import forms


class PoliciesAcceptForm(forms.Form):
    # Define form fields if needed
    pass

class PoliciesAcceptView(LoginRequiredMixin, FormView):
    template_name = 'employee/policies_accept.html'
    form_class = PoliciesAcceptForm
    success_url = reverse_lazy('employee:policies_list')

    def form_valid(self, form):
        policy_slug = self.kwargs['slug']
        policy = Policies.objects.get(slug=policy_slug)
        user = self.request.user

        accepted_policy = UserAcceptedPolicies.objects.create(
            user=user,
            policies=policy,
            accepted=True
        )
        accepted_policy.save()

        return redirect(self.success_url)




class PoliciesListView(ListView):
    model = Policies
    template_name = 'employee/policies_list.html'

class PoliciesDetailView(DetailView):
    model = Policies
    template_name = 'employee/policies_detail.html'
    

class PoliciesAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='admin').exists()

class PoliciesCreateView(PoliciesAdminRequiredMixin, CreateView):
    model = Policies
    template_name = 'employee/policies_create.html'
    fields = ['title', 'description', 'slug']
    success_url = reverse_lazy('employee:policies_list')

class PoliciesUpdateView(PoliciesAdminRequiredMixin, UpdateView):
    model = Policies
    template_name = 'employee/policies_update.html'
    fields = ['title', 'description', 'slug']
    success_url = reverse_lazy('employee:policies_list')

class PoliciesDeleteView(PoliciesAdminRequiredMixin, DeleteView):
    model = Policies
    template_name = 'employee/policies_delete.html'
    success_url = reverse_lazy('employee:policies_list')
