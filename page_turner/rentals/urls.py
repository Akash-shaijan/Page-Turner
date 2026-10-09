from django.urls import path

from .import views

urlpatterns = [
    
    path("rent/<uuid:uuid>/", views.RentBookView.as_view(), name="rent_book"),

    path('my-rents/', views.RentedBookListView.as_view(), name='my_rents'),

    path("admin-rented-details/",views.AdminRentedDetailsView.as_view(), name="admin_rented_details"),
    
    path("mark-returned/<str:uuid>/",views.MarkReturnedView.as_view(), name="mark_returned"),
    
    path('fine/<str:uuid>/', views.FineCalculateView.as_view(), name='fine-calculation'),

    path("admin/rent-requests/", views.RentRequestAdminView.as_view(), name="rent_requests"),
     
    path("admin/rent-requests/<int:rent_id>/<str:action>/", views.RentRequestAdminActionView.as_view(), name="rent_request_action"),
    
    
    path("rentals/userslist/",views.AdminUserListView.as_view(),name="users-list"),
]
