from django.urls import path

from .import views

urlpatterns = [
    
    path('',views.HomeView.as_view(),name='home'),
    
    path('bookcreate/',views.BookCreateView.as_view(),name='bookcreate'),
    
    path('bookedit/<str:uuid>',views.BookEditView.as_view(),name='bookedit'),
    
    path('details/<str:uuid>',views.BookDetailsView.as_view(),name='details'),
    
    path('delete/<str:uuid>',views.BookDeleteView.as_view(),name='detele'),
    
    path('bookread/<str:uuid>',views.BookReadView.as_view(),name='bookread'),
    
 
   
]


