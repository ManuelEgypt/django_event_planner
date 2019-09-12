from django import forms
from django.contrib.auth.models import User
from .models import Event,Booking,Profile,OrgProfile,UserProfile

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username' ,'password']

        widgets={
        'password': forms.PasswordInput(),
        }

class OrganizerForm(forms.ModelForm):
    class Meta:
        model = OrgProfile
        fields = ['org_name','org_description','org_logo']

class UserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name','profile_pic']
        
class SigninForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['owner','slug','available_seats','datetime']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['user','event']


