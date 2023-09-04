from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseForbidden

def csrf_failure_view(request, reason=""):
    # Customize the response for CSRF failure
    return HttpResponseForbidden("CSRF verification failed. Please try again.")