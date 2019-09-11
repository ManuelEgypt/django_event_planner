from django.contrib import admin
from .models import Event,Booking,Profile,OrgProfile,UserProfile
admin.site.register(Event)
admin.site.register(Booking)
admin.site.register(Profile)
admin.site.register(OrgProfile)
admin.site.register(UserProfile)