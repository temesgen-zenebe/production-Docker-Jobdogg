from django.contrib.auth.decorators import login_required  # Import the decorator
from django.shortcuts import render, redirect
from django.views import View
from .forms import TimeAssignedForm, DateAssignedForm, TimeCardForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TimeCard

class TimeCardManagement(LoginRequiredMixin, View):
    
    
    def get(self, request):
        context = {}
        return render(request, 'timeCard/timeCardManagement.html', context)
    
    def post(self, request):
        
        context = {}
        #return redirect('employer:vilificationSandMassage')
        return render(request, 'timeCard/timeCardManagement.html', context)

class TimeCardListView(ListView):
    model = TimeCard
    template_name = 'timeCard/timecard_list.html'  # Create this template later
    context_object_name = 'timecards'

class TimeCardDetailView(DetailView):
    model = TimeCard
    template_name = 'timeCard/timecard_detail.html'  # Create this template later
    context_object_name = 'timecard'


# Assume you have separate views for each form
def create_time_assigned(request):
    if request.method == 'POST':
        form = TimeAssignedForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('timeCard:create_time_card')  # Replace 'success_url' with the URL to redirect to on success
    else:
        form = TimeAssignedForm()
    return render(request, 'timeCard/time_assigned.html', {'form': form})

def create_date_assigned(request):
    if request.method == 'POST':
        form = DateAssignedForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('timeCard:create_time_card')  # Replace 'success_url' with the URL to redirect to on success
    else:
        form = DateAssignedForm()
    return render(request, 'timeCard/date_assigned.html', {'form': form})



@login_required  # Apply the decorator to ensure the user is logged in
def create_time_card(request):
    if request.method == 'POST':
        form = TimeCardForm(request.POST)
        if form.is_valid():
            time_card = form.save(commit=False)  # Save the form data without committing to the database
            time_card.employer = request.user  # Assign the logged-in user as the employer
            time_card.save()  # Save the time_card with the employer information
            return redirect('timeCard:timecard_list')
    else:
        form = TimeCardForm()
    return render(request, 'timeCard/time_card.html', {'form': form})

