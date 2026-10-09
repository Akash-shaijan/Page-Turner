from django.urls import path

from . import views

urlpatterns = [
    
    path("pay-subscription/<str:uuid>/", views.SubscriptionPayView.as_view(), name="subscription_pay"),
    
    path("pay-fine/<str:uuid>/", views.FinePayView.as_view(), name="fine_pay"),
    
    path("razorpay/<str:uuid>/", views.RazorPayView.as_view(), name="razorpay"),
    
    path("verify/", views.PaymentVerifyView.as_view(), name="payment_verify"),
]