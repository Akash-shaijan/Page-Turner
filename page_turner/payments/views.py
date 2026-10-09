from django.shortcuts import render, redirect, get_object_or_404

from django.views import View

from django.utils import timezone

from django.contrib import messages

import razorpay

from decouple import config

from .models import Payment, Transaction

from subscriptions.models import Plan, Subscription

from datetime import timedelta 

from rentals.models import Rent

from subscriptions.utils import EmailService



class SubscriptionPayView(View):
    
    
    def get(self, request, uuid):
        

        # Check pending fine before allowing subscription
        
        pending_fine_rent = next((rent for rent in Rent.objects.filter(user=request.user, fine_paid=False) if rent.is_fine_pending()), None)

        if pending_fine_rent:
            
            messages.error(request, "You have a pending fine!")
            
            return redirect('fine-calculation', uuid=pending_fine_rent.uuid)

        plan = get_object_or_404(Plan, uuid=uuid) 
        
        
        return redirect("razorpay", uuid=plan.uuid)


class FinePayView(View):
    
    
    def get(self, request, uuid):
        

        rent = get_object_or_404(Rent, uuid=uuid)
        
        
        return redirect("razorpay", uuid=rent.uuid)



class RazorPayView(View):
    
    template = "payments/razorpay.html"

    def get(self, request, uuid):
        

        amount = 0
        
        plan = None
        
        plan_query = Plan.objects.filter(uuid=uuid).first()
        
        if plan_query:
            
            plan = plan_query
            
            amount = plan.price
            
             
            request.session["pay_logic"] = "subscription"
            
            request.session.pop("active_fine_rent_uuid", None) 
            
        else:
            
            rent = get_object_or_404(Rent, uuid=uuid)
            
            amount = rent.calculate_fine()
            
            
            request.session["pay_logic"] = "fine"
            
            
            # to understand which fine is paying
            request.session["active_fine_rent_uuid"] = str(rent.uuid)

        # Create the Payment record
        
        payment = Payment.objects.create(user=request.user, plan=plan, amount=amount)

        client = razorpay.Client(auth=(config("RZP_KEY_ID"), config("RZP_KEY_SECRET")))
        
        order_data = {
            
            "amount": int(amount * 100),
            
            "currency": "INR",
            
        }
        rzp_order = client.order.create(data=order_data)

        Transaction.objects.create(
            
            payment=payment,
            
            rzp_order_id=rzp_order.get("id"),
            
            amount=amount
        )

        context = {
            "RZP_KEY_ID": config("RZP_KEY_ID"),
            "amount": rzp_order.get("amount"),
            "order_id": rzp_order.get("id"),
            "payment_uuid": payment.uuid
        }
        return render(request, self.template, context)


class PaymentVerifyView(View):
    
    def post(self, request, *args, **kwargs):

        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        
        razorpay_order_id = request.POST.get("razorpay_order_id")
        
        razorpay_signature = request.POST.get("razorpay_signature")

        client = razorpay.Client(
            
            auth=(config("RZP_KEY_ID"), config("RZP_KEY_SECRET"))
        )

        try:
            #  Verify Razorpay Signature
            client.utility.verify_payment_signature({
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature
            })

            #  Update Transaction
            
            transaction = Transaction.objects.get(rzp_order_id=razorpay_order_id)
            
            transaction.status = "SUCCESS"
            
            transaction.rzp_payment_id = razorpay_payment_id
            
            transaction.rzp_signature = razorpay_signature
            
            transaction.transaction_at = timezone.now()
            
            transaction.save()

            #  Update Payment model
            
            payment = transaction.payment
            
            payment.payment_status = "SUCCESS"
            
            payment.paid_at = timezone.now()
            
            payment.save()

            pay_logic = request.session.pop("pay_logic", None)

            
            #  FINE PAYMENT LOGIC
            
            if pay_logic == "fine":  

                rent_uuid = request.session.pop("active_fine_rent_uuid", None)

                if rent_uuid:
                    
                    rent = Rent.objects.get(uuid=rent_uuid)
                    
                    rent.fine_paid = True
                    
                    rent.fine_paid_at = timezone.now()
                    
                    rent.fine_amount = 0
                    
                    rent.save()

                messages.success(request, "Fine paid successfully!")
                
                return redirect("my_rents")

            
            # SUBSCRIPTION LOGIC
            
            elif pay_logic == "subscription":


                sub, created = Subscription.objects.get_or_create(
                    user=payment.user,
                    defaults={
                        "plan": payment.plan,
                        "start_date": timezone.now(),
                        "end_date": timezone.now() + timedelta(days=payment.plan.duration_days)
                    }
                )

                if not created:
                    
                    if sub.end_date < timezone.now():
                        
                        sub.start_date = timezone.now()
                        
                        sub.end_date = timezone.now() + timedelta(days=payment.plan.duration_days)
                        
                    else:
                        
                        sub.end_date += timedelta(days=payment.plan.duration_days)
                        
                    # After payment is successful, attach that plan to the user's subscription

                    sub.plan = payment.plan 
                    
                    sub.save()

                # EMAIL
                
                email_content = (
                    
                    f"Hi {payment.user },\n\n"
                    
                    f"Your {payment.plan.name} subscription is now active!\n"
                    
                    f"Start Date: {sub.start_date.strftime('%d %B %Y')}\n"
                    
                    f"Expiry Date: {sub.end_date.strftime('%d %B %Y')}\n\n"
                    
                    "Enjoy reading at Page Turner! "
                )

                #Send to Mailinator
                
                success = EmailService.send_notification(to_email="testbox@mailinator.com",subject="Subscription Activated ",message=email_content)

                if success:
                    
                    print("Email sent successfully")
                    
                else:
                    
                    print("Email failed - check SendGrid activity logs")

                messages.success(request, "Subscription activated!")
                
                return redirect("home")

            else:
                
                messages.error(request, "Payment session expired.")
                
                return redirect("home") 
            
        except Exception as e:
            
            print(f"Payment Verification Error: {e}")
            
            messages.error(request, "Payment verification failed.")
            
            return redirect("home")