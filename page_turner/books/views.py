from django.shortcuts import render,redirect

from django.db.models import Q

from django.views import View

from .models import Book

from .forms import BookForm

from subscriptions.models import Plan

from rentals.models import Rent, RentStatus


# Create your views here.


class HomeView(View):
    
    template = 'books/home.html'

    def get(self, request, *args, **kwargs):
        
        books = Book.objects.filter(active_status=True)

        data = {'books': books,'page': 'Home',}

        query = request.GET.get('query')
        
        search_results = None

        if query:
            
            search_results = books.filter(
                
                Q(title__icontains=query) |
                
                Q(description__icontains=query) |
                
                Q(language__name__icontains=query) |
                
                Q(author__name__icontains=query) |
                
                Q(genres__name__icontains=query)
                
                ).distinct()

        plans = Plan.objects.all()

        last_sub = None
        
        end_date = None
        
        new_requests_count = 0

        if request.user.is_authenticated:
           
            last_sub = request.user.subscription_set.order_by('-end_date').first()

            if last_sub and last_sub.is_active:
                
                end_date = last_sub.end_date

            #  Admin count new rent requests
            
            if request.user.is_staff:
                
                new_requests_count = Rent.objects.filter(status=RentStatus.PENDING).count()

        data.update({
            
            'search_results': search_results,
            
            'query': query,
            
            'plans': plans,
            
            'last_sub': last_sub,
            
            'end_date': end_date,
            
            'new_requests_count': new_requests_count,
        })

        return render(request, self.template, context=data)
    
    
    
class BookCreateView(View):

    template = 'books/bookcreate.html'
    
    form_class = BookForm

    def get(self, request, *args, **kwargs):

        form = self.form_class()

        data = {'form': form,'page': 'Create a Book'}

        return render(request, self.template, context=data)

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():

            book = form.save(commit=False)

            # digital safety
            if not book.has_digital:
                
                book.digital_file = None

            book.save()
            
            form.save_m2m()

            return redirect('home')

        data = {'form': form,'page': 'Create a Book'}

        return render(request, self.template, context=data)
    
    
class BookEditView(View):
    
    template = 'books/book-edit.html'
    
    form_class = BookForm

    def get(self, request, *args, **kwargs):
        
        uuid = kwargs.get('uuid')
        
        book = Book.objects.get(uuid=uuid)

        form = self.form_class(instance=book)

        data = {'form': form, 'page': 'Edit a Book'}
        
        return render(request, self.template, context=data)

    def post(self, request, *args, **kwargs):
        
        uuid = kwargs.get('uuid')
        
        book = Book.objects.get(uuid=uuid)

        form = self.form_class(request.POST, request.FILES, instance=book)

        if form.is_valid():
            
            form.save()
            
            return redirect('home')

        data = {'form': form, 'page': 'Edit a Book'}
        
        return render(request, self.template, context=data)

    
    
class BookDetailsView(View):
    
    template = "books/details.html"

    def get(self, request, uuid, *args, **kwargs):
        
        book = Book.objects.get(uuid=uuid)

        last_sub = None
        
        if request.user.is_authenticated:
            
            last_sub = request.user.subscription_set.last()

        data = {"book": book,"last_sub": last_sub,
        }
        return render(request, self.template, context=data)
    
    
class BookDeleteView(View):
    
    def get(self,request,*args,**kwargs):
        
        uuid=kwargs.get('uuid')
        
        book=Book.objects.get(uuid=uuid)
        
        book.active_status=False
        
        book.save()
        
        return redirect('home')
    
    
class BookReadView(View):
    
    template = 'books/book-read.html'

    def get(self, request, *args, **kwargs):
        
        uuid = kwargs.get('uuid')
        
        book = Book.objects.get(uuid=uuid)

        pdf_url = book.digital_file.url 

        data = {
            'book': book,
            
            'pdf_url': pdf_url,
            
            'page': 'read-book'
        }
        
        return render(request, self.template, context=data)

    
    
 
    
    

