from django.db import models

from django.conf import settings

from django.utils import timezone

from datetime import timedelta

from books.models import BaseClass  


class Plan(BaseClass):
    
    name = models.CharField(max_length=100)
    
    price = models.FloatField(default=0)
    
    duration_days = models.IntegerField(default=30)

    def __str__(self):
        
        return self.name


class Subscription(BaseClass):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    
    start_date = models.DateTimeField(default=timezone.now)
    
    end_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        
        if not self.end_date:
            
            self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
            
        super().save(*args, **kwargs)

    def __str__(self):
        
        return f"{self.user.email} - {self.plan.name}"

    @property
    def is_active(self):
        
        return self.end_date >= timezone.now()
    
    
    class Meta:
        
        verbose_name = "Subscription"
        
        verbose_name_plural = "Subscriptions"

