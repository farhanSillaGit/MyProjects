from django.shortcuts import render,redirect,get_object_or_404
from .models import Hotel,Cart,Rooms,Attachments,Emirate,SearchModel,Booking
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BookingUserProfileForm, ClientProfileForm
from django.urls import reverse
from home.tasks import send_booking_confirmation_email
#from taskq.forms import ReviewForm

def index(request):
    emirate=Emirate.objects.all()
    return render(request,'index.html',{'emirate':emirate})

def hotel_list(request):

    hotels=Hotel.objects.all()
    return render(request,'hotel_list.html',{'hotels':hotels})
def hotel_room_list(request):
    rooms=Rooms.objects.all()
    images=Attachments.objects.all()
    return render(request,'rooms.html',{'rooms':rooms,'images':images})


def search_results(request):
    request.session['check_in'] = request.GET.get('check_in', '')
    request.session['check_out'] = request.GET.get('check_out', '')
    request.session['no_of_rooms'] = request.GET.get('no_of_rooms', '')
    request.session['adults'] = request.GET.get('adults', '')
    request.session['children'] = request.GET.get('children', '')

    #check_in=request.GET.get('check_in', '')
    #print(f"check_in")
    query = request.GET.get('q', '')
    ename=Emirate.objects.get(id=query)
    #results = SearchModel.objects.filter(id__icontains=query)
    results = Hotel.objects.filter(emirate_name=query)
    return render(request, 'hotel_list.html', {'results': results, 'query': query,'ename':ename})


def viewroom_action(request,result_id):
    request.session['result_id'] = result_id
    # print(f"check_in")
    images = Attachments.objects.all()
    #results = SearchModel.objects.filter(id__icontains=query)
    results = Rooms.objects.filter(hotel=result_id, check_availability=True)

    return render(request, 'rooms.html', {'rooms': results,'images':images})

@login_required(login_url='login_customer')
def room_booking(request):
    if request.user.is_authenticated:
        check_in = request.session.get('check_in', 'default_value')
        check_out = request.session.get('check_out', 'default_value')
        no_of_rooms = request.session.get('no_of_rooms', 'default_value')
        adults = request.session.get('adults', 'default_value')
        children = request.session.get('children', 'default_value')
        room_id= request.GET.get('room_id', '')

        room = get_object_or_404(Rooms, id=room_id)


        room_type = room.room_type
        hotel_name=room.hotel
        print(f"room type", room_type)
        print(f"hotel name", hotel_name)
        booking_data = {
            'user': request.user,
            'room_id': room_id,
            'check_in': check_in,
            'check_out': check_out,
            'no_of_rooms': no_of_rooms,
            'adults': adults,
            'children': children,
        }

        try:
            booking = Booking.objects.create(**booking_data)
            email = request.user.email
            send_booking_confirmation_email.delay(booking.id,email)
            messages.success(request, 'Booking successful!')
            return render(request, 'booking_success.html', {'booking': booking,'room_type':room_type,'hotel_name':hotel_name})
        except Exception as e:


            messages.error(request, f'Error during booking: {str(e)}')
            return render(request, 'booking_error.html')

    else:

        # User is not signed in, redirect to the login page

        return redirect('login')


#registration
def register_customer(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            #messages.success(request, 'Registration successful! Welcome!')

            if user.is_client:
                return redirect('create_client_profile')
            else:
                return redirect('create_booking_user_profile')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    return render(request, 'register_customer.html', {'form': form})

def login_customer(request):

    if request.method == 'POST':
        # Handle login form submission
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Attempting to authenticate user: {username}")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Check if the user was attempting to make a booking
            if any(request.session.get(key) for key in ['check_in', 'check_out', 'no_of_rooms', 'adults', 'children']):
                # Redirect to the booking page
                result_id = request.session.get('result_id', 'default_value')
               # print(f"result_id",result_id)
                return redirect('viewroom_action',result_id=result_id)

            # Clear the booking session variables
            #for key in ['check_in', 'check_out', 'no_of_rooms', 'adults', 'children']:
               # del request.session[key]


            if user.is_client:
                return redirect('client_dashboard')
            else:
                return redirect('index')
        else:
            # Authentication failed, show an error message

            messages.error(request, 'Invalid login credentials')
            return render(request, 'login.html')

    # If the request method is GET, render the login form
    messages.info(request, 'Please log in to access your account.')
    return render(request, 'login.html')

def logout_customer(request):
    logout(request)
    return redirect('index')

#profile creation


#@login_required
def create_booking_user_profile(request):
    if request.method == 'POST':
        form = BookingUserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('booking_user_dashboard')  # Adjust the redirect as needed
        else:
                print(form.errors)
    else:
        form = BookingUserProfileForm()

    return render(request, 'create_booking_user_profile.html', {'form': form})

#@login_required
def create_client_profile(request):
    if request.method == 'POST':
        form = ClientProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            hotel_id = profile.hotel_id
            return redirect('client_dashboard')  # Adjust the redirect as needed
        else:
                print(form.errors)
    else:
        form = ClientProfileForm()

    return render(request, 'create_client_profile.html', {'form': form})


from .models import BookingUserProfile,ClientProfile

@login_required
def booking_user_dashboard(request):
    booking_history = Booking.objects.filter(user=request.user).order_by('-booking_date_time')
    user_profile = BookingUserProfile.objects.get(user=request.user)
    return render(request, 'booking_user_dashboard.html', {'user_profile': user_profile,'booking_history':booking_history})
@login_required
def client_dashboard(request):
    user_profile = get_object_or_404(ClientProfile, user=request.user)

    # Access the hotel_id from the ClientProfile
    hotel_id = user_profile.hotel_id.id
    #print(f"Hotel ID: {hotel_id}")

    recent_booking = Booking.objects.filter(room__hotel_id=hotel_id).order_by('-booking_date_time')
    #print(f"Recent Bookings: {recent_booking}")
    user_profile = ClientProfile.objects.get(user=request.user)

    # Fetch all room types
    all_room_types = Rooms.objects.filter(hotel_id=hotel_id).values_list('room_type', flat=True)
    print(f"all room types: {all_room_types}")
    if request.method == 'POST':
        # Handle the form submission
        selected_room_types = request.POST.getlist('room_types[]')
        print(f"Selected room types: {selected_room_types}")
        # Perform your logic to update availability for the selected room types
        for room_type in all_room_types:

            print(f"Checking room type: {room_type}")
            room = Rooms.objects.get(room_type=room_type)
            print(f"Checking room : {room}")
            # Update availability logic here
            if room_type in selected_room_types:
                print(f"Checking room status : {room.check_availability}")

                room.check_availability = False
                print(f"Checking room status : {room.check_availability}")
            else:
                room.check_availability = True

            room.save()

        success_url = reverse('client_dashboard') + '?success=true'
        return redirect(success_url)  # Redirect to the client dashboard with success message

    return render(request, 'client_dashboard.html', {'user_profile': user_profile,'recent_booking':recent_booking, 'all_room_types': all_room_types})

@login_required
def edit_client_profile(request):
    client_profile = request.user.clientprofile

    if request.method == 'POST':
        form = ClientProfileForm(request.POST, instance=client_profile)
        if form.is_valid():
            form.save()
            return redirect('client_dashboard')  # Redirect to the user's profile page
    else:
        form = ClientProfileForm(instance=client_profile)

    return render(request, 'edit_client_profile.html', {'form': form})

@login_required
def edit_booking_user_profile(request):
    booking_user_profile = request.user.bookinguserprofile

    if request.method == 'POST':
        form = BookingUserProfileForm(request.POST, instance=booking_user_profile)
        if form.is_valid():
            form.save()
            return redirect('booking_user_dashboard')  # Redirect to the user's profile page
    else:
        form = BookingUserProfileForm(instance=booking_user_profile)

    return render(request, 'edit_booking_user_profile.html', {'form': form})

