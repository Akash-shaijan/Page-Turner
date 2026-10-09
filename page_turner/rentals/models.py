from django.db import models

from django.utils import timezone

from datetime import timedelta

from django.conf import settings

from books.models import BaseClass


class RentStatus(models.TextChoices):
    
    PENDING = 'pending', 'Pending'
    
    APPROVED = 'approved', 'Approved'
    
    REJECTED = 'rejected', 'Rejected'
    
    RETURNED = 'returned', 'Returned'


class Rent(BaseClass):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="rents" )

    book = models.ForeignKey("books.Book",on_delete=models.CASCADE,related_name="rents")

    status = models.CharField(max_length=10,choices=RentStatus.choices,default=RentStatus.PENDING)

    request_date = models.DateTimeField(auto_now_add=True)
    
    rent_date = models.DateTimeField(null=True, blank=True)
    
    due_date = models.DateTimeField(null=True, blank=True)
    
    return_date = models.DateTimeField(null=True, blank=True)

    fine_amount = models.DecimalField(default=0,max_digits=10,decimal_places=2)
        
    fine_paid = models.BooleanField(default=False)
    
    fine_paid_at = models.DateTimeField(null=True, blank=True)
    

    def approve(self, days=7):
        
        self.status = RentStatus.APPROVED
        
        self.rent_date = timezone.now()
        
        self.due_date = timezone.now() + timedelta(days=days)
        
        self.save()

    def mark_returned(self):
        
        self.return_date = timezone.now()
        
        self.fine_amount = self.calculate_fine()
        
        self.status = RentStatus.RETURNED
        
        self.save()

    def calculate_fine(self):
        
        if not self.return_date or not self.due_date:
            
            return 0

        if self.return_date > self.due_date: 
            
            days_late = (self.return_date.date() - self.due_date.date()).days
            
            return days_late * 10

        return 0
    
    
    def is_fine_pending(self):
    
        return self.calculate_fine() > 0 and not self.fine_paid

    def __str__(self):
        
        return f"{self.user} - {self.book.title} ({self.get_status_display()})"
