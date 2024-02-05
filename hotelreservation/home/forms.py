from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class UserRegistrationForm(UserCreationForm):
    email= forms.EmailField(required=True)
    class Meta:

        model = User
        fields = ['username','email', 'password1','password2']
       # fields = UserCreationForm.Meta.fields + ('email',)
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Confirm Password'
                }


# forms for two customer




from .models import BookingUserProfile, ClientProfile

class BookingUserProfileForm(forms.ModelForm):
    class Meta:
        model = BookingUserProfile
        fields = ['full_name','address', 'date_of_birth', 'nationality', 'place', 'profile_picture', 'phone_number']

class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ['hotel_id', 'emirate_id', 'phone_number', 'place','license_no','sponsor_name','owner_name']

# adding client check
from .models import CustomUser

# check for newcustom+
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email','is_client', 'is_booking_user')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_client = self.cleaned_data['is_client']
        user.is_booking_user = self.cleaned_data['is_booking_user']
        if commit:
            user.save()
        return user

