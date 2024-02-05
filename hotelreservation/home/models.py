from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User,AbstractUser
# Create your models here.
class Emirate(models.Model):
    emirate_name = models.CharField(max_length=100)
    def __str__(self):
        return self.emirate_name
class Hotel(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    #price=models.DecimalField(max_digits=8,decimal_places=2)
    hotelimg=models.ImageField(upload_to='hotels',null=True)
    emirate_name = models.ForeignKey(Emirate, on_delete=models.CASCADE)
    special_offer = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Rooms(models.Model):

    room_type=models.CharField(max_length=100)
    description=models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    check_availability=models.BooleanField(default=True)
    hotel= models.ForeignKey(Hotel, on_delete=models.CASCADE)
    #room_img= models.ImageField(upload_to='rooms', null=True)
    def __str__(self):
        return self.hotel_name

    def __str__(self):
        return self.room_type

class Attachments(models.Model):

    room = models.ForeignKey(Rooms,on_delete=models.CASCADE)
   # room_type = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_image = models.ImageField(upload_to='rooms',null=True)


class Cart(models.Model):
    name=models.ForeignKey(Hotel,on_delete=models.CASCADE)

class SearchModel(models.Model):

    destination = models.CharField(max_length=255)


# models for two type customers


#from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )
    #is_client = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_booking_user = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_client and self.is_booking_user:
            raise ValueError("A user cannot be both a client and a booking user.")
        super().save(*args, **kwargs)
    pass

class BookingUserProfile(models.Model):
    user = models.OneToOneField(CustomUser,null=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255,null=True)
    #email = models.EmailField(default=None)
    address = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='uploads/customer_profile_pics/', blank=True)
    phone_number = models.CharField(max_length=15)



class ClientProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    emirate_id = models.ForeignKey(Emirate, on_delete=models.CASCADE)
    #email = models.EmailField(default=None)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    place = models.CharField(max_length=255)
    license_no =models.CharField(default=None,max_length=255)
    sponsor_name=models.CharField(default=None,max_length=255)
    owner_name=models.CharField(default=None,max_length=255)

class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    no_of_rooms = models.IntegerField()
    adults = models.IntegerField()
    children = models.IntegerField()
    booking_date_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Booking for {self.user.username} - Room {self.room}"











