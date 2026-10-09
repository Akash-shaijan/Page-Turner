from django.shortcuts import render

# Create your views here.

from django.shortcuts import render,redirect

from django.views import View

from .models import Rent,RentStatus

from django.shortcuts import get_object_or_404

from django.contrib import messages

from django.utils import timezone

from datetime import timedelta

from django.shortcuts import get_object_or_404, redirect, render

from books.models import Book

from payments.models import Payment, Transaction

import razorpay

from decouple import config

from subscriptions.models import Subscription

from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.


class RentBookView(View):
    
    template = 'rentals/rentbook.html'

    def post(self, request, uuid):
        

        book = get_object_or_404(Book, uuid=uuid)
        
        user = request.user


        #  CHECK FOR ACTIVE SUBSCRIPTION 
  
        active_sub = Subscription.objects.filter(user=user, end_date__gt=timezone.now()).first()

        if not active_sub:
            
            messages.error(request, "You need an active subscription to rent books.")
            
            return redirect('subscription_plans')


        #  CHECK FOR PENDING FINES


        pending_fines = [
            
            rent for rent in Rent.objects.filter(user=user, fine_paid=False) 
            
            if rent.is_fine_pending()
        ]

        if pending_fines:
            
            messages.error(request, "Access Denied: You have unpaid fines. Please clear them first.")
            
            # Redirect to the first pending fine found
            
            return redirect('fine-calculation', uuid=pending_fines[0].uuid)
     
        
        # Check if user already has a request for this book
        
        existing_rent = Rent.objects.filter(user=user,book=book,status__in=[RentStatus.PENDING, RentStatus.APPROVED]).first()

        if existing_rent:
            
            return render(request, self.template, {'book': book, 'rent': existing_rent})

        # Check availability of copies
        
        if book.available_copies <= 0:
            
            messages.error(request, "This book is currently not available.")
            
            return redirect('details', uuid=uuid)

        # Create new rent 
        
        rent = Rent.objects.create(user=user,book=book,status=RentStatus.PENDING)

        return render(request, self.template, {'book': book, 'rent': rent})

    def get(self, request, uuid):
        
        if not request.user.is_authenticated:
            
            return redirect('login')

        book = get_object_or_404(Book, uuid=uuid)
        
        rent = Rent.objects.filter(user=request.user,book=book,status__in=[RentStatus.PENDING, RentStatus.APPROVED]).first()

        return render(request, self.template, {'book': book, 'rent': rent})


class RentedBookListView(View):

    template = "rentals/list-rented-books.html"

    def get(self, request, *args, **kwargs):

        rents = (Rent.objects.filter(user=request.user).select_related("book").order_by("-request_date"))

        data = {"rents": rents,"now": timezone.now(),}

        return render(request, self.template, context=data)


class AdminRentedDetailsView(View):
    
    template = "rentals/admin-rented-details.html"

    def get(self, request):

        rents = (Rent.objects.select_related("user", "book").exclude(status=RentStatus.REJECTED).order_by("-request_date"))  

        return render(request, self.template, {"rents": rents,"now": timezone.now()})

    
    


class RentRequestAdminView(View):
    
    template = "rentals/rent_requests.html"

    def get(self, request):

        pending_rents = Rent.objects.filter(status=RentStatus.PENDING).order_by("-request_date")
        
        return render(request, self.template, {"rents": pending_rents})

    
class RentRequestAdminActionView(View):
    
    def post(self, request, rent_id, action):
        

        rent = get_object_or_404(Rent, id=rent_id)


        if action == "approve":

            rent.status = RentStatus.APPROVED
            
            rent.rent_date = timezone.now()
            
            rent.due_date = timezone.now() + timedelta(days=7)
            
            rent.save()

            # Reduce available copies 
            
            if rent.book.has_physical:
                
                rent.book.available_copies -= 1
                
                rent.book.save()

            messages.success(request, f"Rent request for '{rent.book.title}' approved.")

        elif action == "reject":
            
            rent.status = RentStatus.REJECTED
            
            rent.save()
            
            messages.error(request, f"Rent request for '{rent.book.title}' rejected.")

        else:
            
            messages.error(request, "Invalid action.")

        return redirect("rent_requests")



class MarkReturnedView(View):

    def post(self, request, uuid):

        rent = get_object_or_404(Rent, uuid=uuid)
        
        # Only APPROVED books can be returned 
        
        if rent.status != RentStatus.APPROVED:
            
            messages.warning(request, "This book cannot be marked as returned.")
            
            return redirect("admin_rented_details")

        # Update rent
        
        rent.status = RentStatus.RETURNED
        
        rent.return_date = timezone.now()
        
        rent.fine_amount = rent.calculate_fine()  # calculate fine
        
        rent.save()

        # Increase book availability
        
        if rent.book.has_physical:
            
            rent.book.available_copies += 1
            
            rent.book.save()

        messages.success(request,f"Book '{rent.book.title}' marked as returned.")

        return redirect("admin_rented_details")
    
    

class AdminUserListView(View):
    
    template_name = "rentals/users_list.html"

    def get(self, request):

        users = User.objects.all().order_by("-date_joined")

        user_data = []
        
        for user in users:
            
            subscription = Subscription.objects.filter(user=user,active_status=True).first()

            user_data.append({ "user": user, "subscription": subscription})

        return render(request,self.template_name,{"user_data": user_data})

    def post(self, request):
        

        user_id = request.POST.get("user_id")

        user = get_object_or_404(User, id=user_id)

        # prevent admin from deactivating themselves
        
        if user == request.user:
            
            messages.error(request, "You cannot deactivate your own account.")
            
            return redirect("users-list")

        user.is_active = False
        
        user.save()

        messages.success(request, f"User '{user.email}' deactivated successfully.")
        
        return redirect("users-list")


    


class FineCalculateView(View):
    
    template_name = "rentals/fine-calculation.html"

    def get(self, request, uuid):
        
        rent = get_object_or_404(Rent, uuid=uuid)

        if rent.fine_paid:
            
            fine_amount = 0
            
            messages.info(request, "Fine already paid.")
            
        else:
            
            fine_amount = rent.calculate_fine()

       
        return render(request, self.template_name, {"rent": rent,"fine_amount": fine_amount})





