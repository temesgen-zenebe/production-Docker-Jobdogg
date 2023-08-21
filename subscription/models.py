# subscription/models.py
from django.db import models
from common.utils.text import unique_slug
from jobDoggApp import settings


class SubscriptionPlan(models.Model):
    """
    Represents different subscription plans with their names, prices, and durations.
    """
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self.name, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    """
    Represents a user's subscription.
    Connects to the User model via a one-to-one relationship.
    Relates to a specific SubscriptionPlan to indicate the chosen plan.
    Tracks the start and end dates of the subscription.
    Tracks whether the subscription is active or not.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"

class PaymentTerm(models.Model):
    """
    Represents payment terms for Billing and payment.
    payment term (e.g., "Net 30", "Due on Receipt").
    """
    name = models.CharField(max_length=100)
    days_to_due = models.IntegerField()
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self.name, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Billing(models.Model):
    """
    Represents an invoice issued to a customer.
    Connects to the User model to associate invoices with customers.
    Includes details such as the invoice amount, due date, and payment status.
    Relates to a PaymentTerm model for setting up payment terms.
    """
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    payment_term = models.ForeignKey(PaymentTerm, on_delete=models.SET_NULL, blank=True, null=True)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self.customer, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.username} - {self.amount}"
    
class CustomerBillingInfo(models.Model):
    """
    Stores customer's billing information.
    """
    customer = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    billing_address = models.TextField()
    payment_method = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self.customer.username, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.customer.username

class PaymentStatus(models.Model):
    """
    Represents payment statuses.
    Name: "Pending" , Description: "Payment is pending and hasn't been processed yet."
    Name: "Paid" , Description: "Payment has been successfully processed and received."
    Name: "Failed". Description: "Payment processing has failed, and the payment was not successful."
    Name: "Refunded" ,Description: "The payment amount has been refunded to the customer."
    Name: "Overdue", Description: "Payment is overdue and hasn't been made by the due date."
    """
    name = models.CharField(max_length=50)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Payment(models.Model):
    """
    Represents a payment made by a customer.
    Connects to the Billing model to associate payments with specific invoices.
    Tracks payment details such as the payment amount, date, and method.
    Relates to a PaymentStatus model to indicate the status of the payment.
    """
    invoice = models.ForeignKey(Billing, on_delete=models.CASCADE)
    payment_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_status = models.ForeignKey(PaymentStatus, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self.invoice.customer, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.invoice.customer.username} - {self.amount}"


