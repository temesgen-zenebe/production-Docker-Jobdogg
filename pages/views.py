from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import render,redirect


class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutUsView(TemplateView):
    template_name = 'pages/about_us.html'

    def get(self, request, *args, **kwargs):
        messages.debug(request, 'Debug message.')
        messages.info(request, 'Info message.')
        messages.success(request, 'Success message.')
        messages.warning(request, 'Warning message.')
        messages.error(request, 'Error message.')
        return super().get(request, args, kwargs)
    
class ContactUsView(TemplateView):
    template_name = 'pages/contact_us.html'


def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'pages/dashboard.html')
    else:
        return redirect('login')




    