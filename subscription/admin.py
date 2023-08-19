# subscription/admin.py
from django.contrib import admin
from .models import SubscriptionPlan, Subscription, Billing, Payment, PaymentStatus, PaymentTerm, CustomerBillingInfo

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days')
    

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'is_active')

@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'amount', 'due_date', 'is_paid', 'payment_term')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'payment_date', 'amount', 'payment_method', 'payment_status')

@admin.register(PaymentStatus)
class PaymentStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(PaymentTerm)
class PaymentTermAdmin(admin.ModelAdmin):
    list_display = ('name', 'days_to_due')
   

@admin.register(CustomerBillingInfo)
class CustomerBillingInfoAdmin(admin.ModelAdmin):
    list_display = ('customer', 'billing_address', 'payment_method')
   
