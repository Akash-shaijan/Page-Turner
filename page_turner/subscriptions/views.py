from django.shortcuts import render

# Create your views here.

from django.views import View

from .models import Plan

class PlanListView(View):
    
    template="subscriptions/plans.html"
    
    def get(self, request):
        
        plans = Plan.objects.all()
        
        data={'plans':plans}
        
        return render(request,self.template,context=data)
    
    

