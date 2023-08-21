# subscription/views.py
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views import View
from .models import  SubscriptionPlan, Subscription, Billing, Payment, PaymentStatus
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
class UserDashboardView(View):
    def get(self, request):
        user_subscriptions = Subscription.objects.filter(user=request.user)
        user_invoices = Billing.objects.filter(customer=request.user)
        context = {
            'user_subscriptions': user_subscriptions,
            'user_invoices': user_invoices,
        }
        return render(request, 'subscription/user_dashboard.html', context)
    
@method_decorator(login_required, name='dispatch')
class SubscriptionCreateView(View):
    def get(self, request):
        subscription_plans = SubscriptionPlan.objects.all() 
        Billing_creation = Billing.objects.all() 
        context = {
            'subscription_plans': subscription_plans,
            'Billing_creation':Billing_creation
        }
        return render(request, 'subscription/subscription_create.html', context)
    
    def post(self, request):
                plan_id = request.POST.get('plan_id')
                selected_plan = SubscriptionPlan.objects.get(id=plan_id)
                
                # Calculate start and end dates
                start_date = datetime.now().date()  # Current date as the start date
                end_date = start_date + timedelta(days=selected_plan.duration_days)
                
                # Create the subscription
                subscription = Subscription.objects.create(
                    user=request.user,
                    plan=selected_plan,
                    start_date=start_date,
                    end_date=end_date,
                    is_active=True
                )
                billing = Billing.objects.create(
                    customer=request.user,
                    amount=selected_plan.price,
                    due_date = end_date,
                    is_paid = False,
                    
                    
                )
                # You can add further logic like sending confirmation emails, etc.
                return redirect('subscription:user_dashboard')  # Redirect to user dashboard
    
@method_decorator(login_required, name='dispatch')
class PaymentProcessView(View):
    def get(self, request, slug):
        billing = Billing.objects.get(slug=slug)
        payment_statuses = PaymentStatus.objects.all()
        context = {
            'billing': billing,
            'payment_statuses': payment_statuses,
        }
        return render(request, 'subscription/payment_process.html', context)

    def post(self, request, slug):
        billing = Billing.objects.get(slug=slug)
        payment_status_id = request.POST.get('payment_status_id')  # Get selected payment status ID
        payment_status = PaymentStatus.objects.get(id=payment_status_id)
        
        # Create the payment
        payment = Payment.objects.create(
            invoice=billing,
            payment_date=timezone.now(),
            amount=billing.amount,
            payment_method='Credit Card',  # You can change this based on user input
            payment_status=payment_status
        )
        
        # Update billing status and other necessary actions
        
        return redirect('subscription:user_dashboard')  # Redirect to user dashboard
