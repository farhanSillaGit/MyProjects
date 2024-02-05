"""
URL configuration for hotelreservation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from home.views import hotel_list,hotel_room_list,search_results,viewroom_action,register_customer,login_customer,\
    logout_customer,booking_user_dashboard,create_booking_user_profile,create_client_profile,index,\
    client_dashboard,room_booking,edit_client_profile,edit_booking_user_profile
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',index,name='index'),
    path('',include('home.urls')),
    path('hotels/',hotel_list,name='hotel_list'),
    path('rooms/',hotel_room_list,name='rooms_list'),
    path('search/', search_results, name='search_results'),
    path('viewroom/<int:result_id>/', viewroom_action, name='viewroom_action'),
    path('register/', register_customer, name='register_customer'),
    path('login/', login_customer, name='login_customer'),
    path('logout/', logout_customer, name='logout_customer'),
    path('create-booking-user-profile/', create_booking_user_profile, name='create_booking_user_profile'),
    path('create-client-profile/', create_client_profile, name='create_client_profile'),
    path('booking-user-dashboard/', booking_user_dashboard, name='booking_user_dashboard'),
    path('client-dashboard/', client_dashboard, name='client_dashboard'),
    path('book/', room_booking, name='room_booking'),
    path('room-booking/', login_required(room_booking, login_url='login_customer'), name='room_booking'),
    path('edit_client_profile/',edit_client_profile,name='edit_client_profile'),
    path('edit_booking_user_profile/',edit_booking_user_profile,name='edit_booking_user_profile'),




] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
