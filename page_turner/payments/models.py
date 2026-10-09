from django.db import models

from django.conf import settings

from django.utils import timezone

from books.models import BaseClass  

from subscriptions.models import Plan



class Payment(BaseClass):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True)
    
    amount = models.FloatField(default=0)
    
    payment_status = models.CharField(max_length=20,choices=[("PENDING","Pending"), ("SUCCESS","Success"), ("FAILED","Failed")],default="PENDING")
    
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        
        if self.plan:
            
            return f"{self.user.email} - {self.plan.name}"
        
        return f"{self.user.email} - Fine Payment"




class Transaction(BaseClass):
    
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)

    rzp_order_id = models.CharField(max_length=100)
    
    rzp_payment_id = models.CharField(max_length=100, null=True, blank=True)
    
    rzp_signature = models.CharField(max_length=255, null=True, blank=True)

    amount = models.FloatField()
    
    status = models.CharField( max_length=20, choices=[("PENDING","Pending"), ("SUCCESS","Success"), ("FAILED","Failed")], default="PENDING")
    
    transaction_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        
        return f"{self.payment.user.email} - {self.status}"

