from django.urls import path

from .views import PlanListView

urlpatterns = [
    
    path("", PlanListView.as_view(), name="subscription_plans"),
]
