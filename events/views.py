from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import SignupForm,SigninForm,EventForm,BookingForm,OrganizerForm,UserForm
from .models import Event,Booking,Profile,OrgProfile,UserProfile
from datetime import datetime,date
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from django.http import Http404
from django.core.mail import send_mail
from django.conf import settings

def email(request):
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['manuelnasif@gmail.com',]
    send_mail( subject, message, email_from, recipient_list )
    return redirect('app:home')


def home(request):
    return render(request,'home.html')


def no_access(request):
    return render(request,'no_access.html')


def signup(request):
    #permission ---start---
    if not request.user.is_anonymous:   
        return redirect('app:no-access')
    #permision ----end-----
    form = SignupForm()
    user_form = UserForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        user_form = UserForm(request.POST,request.FILES)
        if form.is_valid() and user_form.is_valid():
            main_obj = form.save(commit=False)
            main_obj.set_password(main_obj.password)
            main_obj.save()
            login(request,main_obj)
            profile_obj = Profile(user=main_obj,is_organiser=False)
            profile_obj.save()
            user_obj = user_form.save(commit=False)
            user_obj.user = main_obj
            user_obj.profile = profile_obj
            user_obj.save()
            messages.success(request, 'Welcome %s!' %(user_obj.full_name))
            print(request.user.profile.is_organiser)
            return redirect('app:list')

    context = {                             
        "form": form,
        "user_form": user_form
    }
    return render(request,'signup.html',context)


def org_signup(request):
    #permission ---start---
    if not request.user.is_anonymous:   
        return redirect('app:no-access')
    #permision ----end-----
    form = SignupForm()
    org_form = OrganizerForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        org_form = OrganizerForm(request.POST,request.FILES)
        if form.is_valid() and org_form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.set_password(user_obj.password)
            user_obj.save()
            login(request,user_obj)
            profile_obj = Profile(user=user_obj,is_organiser=True)
            profile_obj.save()
            org_obj = org_form.save(commit=False)
            org_obj.user = user_obj
            org_obj.profile = profile_obj
            org_obj.save()
            messages.success(request, 'Welcome %s!' %(org_obj.org_name))
            return redirect('app:dashboard')
    context = {
        "form": form,
        "org_form": org_form
    }
    return render(request,'organization_signup.html',context)



def signin(request):
    #permission ---start---
    if not request.user.is_anonymous:   
        return redirect('app:no-access')
    #permision ----end-----
    form= SigninForm()
    if request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            my_username = form.cleaned_data['username']  
            my_password = form.cleaned_data['password']            
            user_obj = authenticate(username=my_username, password=my_password)
            if user_obj is not None:
                login(request,user_obj)
                if request.user.profile.is_organiser:
                    messages.success(request,'Welcome back %s!' %(user_obj.profile.orgprofile.org_name))
                    return redirect('app:') 
                else:
                    messages.success(request,'Welcome back %s!' %(user_obj.profile.userprofile.full_name))
                    return redirect('app:list') 
            messages.warning(request,'incorrect username/password!')
    context={
        "form":form,
    }
    return render(request, 'signin.html', context)


def signout(request):
    #permission ---start---
    if request.user.is_anonymous: 
        return redirect('app:no-access')
    #permision ----end-----
    logout(request)
    return redirect('app:signin')


def event_list(request):
    #permission ---start---
    if request.user.is_anonymous: 
        messages.success (request, "Please sign in!")
        return redirect('app:signin')
    #permision ----end-----
    #permission ---start---
    if request.user.profile.is_organiser:
        return redirect('app:no-access')
    #permision ----end-----
    events = Event.objects.filter(datetime__gte=timezone.now())
    query = request.GET.get('q')
    if query:
        events = events.filter(
            Q(name__icontains=query)|
            Q(description__icontains=query)|
            Q(owner__profile__orgprofile__org_name__icontains=query)
        ).distinct()
    context = {
        "events": events
    }
    return render(request,'list.html',context)


def dashboard(request):
    #permission ---start---
    if request.user.is_anonymous:
        messages.success (request, "Please sign in!")
        return redirect('app:signin')
    #permision ----end-----
    if not request.user.profile.is_organiser:
        return redirect('app:no-access')
    #permision ----end-----
    profile_obj = request.user.profile
    user_obj =request.user
    organiser_obj = request.user.profile.orgprofile
    followers_count = UserProfile.objects.filter(orgprofile=organiser_obj).count()
    if profile_obj.is_organiser:
        past_events = user_obj.events.filter(datetime__lt=datetime.now())
        upcoming_events = user_obj.events.filter(datetime__gte=datetime.now())
    context = {
        "past_events": past_events,
        "upcoming_events": upcoming_events,
    }
    return render(request,'dashboard.html',context)


def event_detail(request,event_slug):
    #permission ---start---
    if request.user.is_anonymous:
        messages.success (request, "Please sign in!")
        return redirect('app:signin')
    #permision ----end-----
    event_obj = Event.objects.get(slug=event_slug)
    bookings = Booking.objects.filter(event=event_obj)
    print(event_obj.is_past())
    context = {
        "event": event_obj,
        "bookings": bookings,
    }
    return render(request,'detail.html', context)


def event_create(request):
    #permission ---start---
    if request.user.is_anonymous:   
        messages.success (request, "Please sign in!")
        return redirect('app:signin')
    #permision ----end-----
    #permission ---start---
    if not request.user.profile.is_organiser:
        return redirect('app:no-access')
    #permision ----end-----
    form = EventForm()  
    if request.method == "POST":                             
        form = EventForm(request.POST, request.FILES)     
        if form.is_valid():                                 
            event_obj = form.save(commit=False)             
            event_obj.owner = request.user 
            event_obj.available_seats = event_obj.seats  
            event_obj.datetime = datetime.combine(event_obj.date,event_obj.time)
            if event_obj.datetime < datetime.now():
                messages.warning (request, "Are you trying to make an event in the past! Are you drunk?!")
                return redirect('app:create')
            event_obj.save()
            subject = "%s is organising a new event: '%s'"% (event_obj.owner.profile.orgprofile.org_name,event_obj.name)
            message = "%s will be taking place in %s on %s, \nMore Details: %s"%(event_obj.name,event_obj.location,event_obj.datetime,event_obj.description)
            email_from = settings.EMAIL_HOST_USER
            sender_list = list(UserProfile.objects.filter(orgprofile=request.user.profile.orgprofile))
            e_sender_list = []
            for sender in sender_list:
                e_sender_list.append(sender.profile.user.email)
            followers_list = UserProfile.objects.filter(orgprofile=request.user.profile.orgprofile)
            recipient_list = e_sender_list
            send_mail( subject, message, email_from, recipient_list )
                                
            messages.success (request, "new event %s added successfully" %(event_obj.name))
            return redirect('app:dashboard')                         
    context = {
        "form": form                                        
    }
    return render(request,'create.html', context)


def booking_create(request,event_slug):
     #permission ---start--- 
    if request.user.is_anonymous:   
        messages.success (request, "Please sign in!")
        return redirect('app:signin')
    #permision ----end-----
    event_obj = Event.objects.get(slug=event_slug)
    #permission ---start--- 
    if event_obj.datetime < timezone.now():   
        return redirect ('app:no-access')
    #permision ----end-----
    #permission ---start---
    if request.user.profile.is_organiser:
        return redirect('app:no-access')
    #permision ----end-----
    event_obj = Event.objects.get(slug=event_slug)
    if event_obj.is_full():
        return redirect ('app:detail', event_slug)
    form = BookingForm()
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking_obj = form.save(commit=False)
            booking_obj.event = event_obj
            booking_obj.user = request.user
            msg = booking_obj.book_seat()
            if msg == True:
                booking_obj.save()
                event_obj.save()
                subject = "Successfully booked %s seats for the '%s' event"% (booking_obj.desired_seats,event_obj.name)
                message = "%s will be taking place in %s on %s, \nMore Details: %s"%(event_obj.name,event_obj.location,event_obj.datetime,event_obj.description)
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.user.email]
                send_mail( subject, message, email_from, recipient_list )
                messages.success (request, "Successfully booked %s seat(s) for %s" %(booking_obj.desired_seats,event_obj.name))
            else:
                messages.warning (request, "You requested %s seats, only %s seats available for %s" %(booking_obj.desired_seats,event_obj.available_seats,event_obj.name))
                return redirect ('app:booking-create', event_slug)
            return redirect ('app:detail', event_slug)
    context = {
        "form": form,
        "event": event_obj
    }
    return render(request, 'booking_create.html', context)


def event_update(request,event_slug):
    event = Event.objects.get(slug=event_slug)
    #permission ---start---
    if request.user != event.owner:  
        return redirect('app:no-access')
    #permision ----end-----
    #permission ---start--- 
    if event.datetime < timezone.now():   
        return redirect ('app:no-access')
    #permision ----end-----
    form = EventForm(instance=event)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event_obj = form.save(commit=False)
            date_time=datetime.combine(event_obj.date,event_obj.time)
            if date_time < datetime.now():
                messages.info (request, "cannot modify event to be in the past")
                return redirect ('app:update', event_slug)
            else:
                form.save()
                messages.info (request, "event updated successfully")
                return redirect (event_obj)
    context = {
        "form" : form,
        "event": event
    }
    return render (request,'update.html',context)


def update_user(request):
    #permission ---start---
    if request.user.is_anonymous:   
        return redirect('app:no-access')
    #permision ----end-----
    profile_obj = request.user.profile
    #permission ---start---
    if profile_obj.is_organiser:   
        return redirect('app:no-access')
    #permision ----end-----
    form = SignupForm(instance=request.user)
    user_form = UserForm(instance=request.user.profile.userprofile)
    if request.method == "POST":
        form = SignupForm(request.POST,instance=request.user)
        user_form = UserForm(request.POST,request.FILES,instance=request.user.profile.userprofile)
        if form.is_valid() and user_form.is_valid():
            main_obj = form.save(commit=False)
            main_obj.set_password(main_obj.password)
            main_obj.save()
            login(request,main_obj)
            user_obj = user_form.save(commit=False)
            user_obj.user = main_obj
            user_obj.save()
            messages.success(request, 'Your profile has been updated, %s!' %(user_obj.full_name))
            return redirect('app:user-profile',request.user.profile.userprofile.slug)

    context = {                             
        "form": form,
        "user_form": user_form
    }
    return render(request,'update_user.html',context)


def update_organiser(request):
    #permission ---start---
    if request.user.is_anonymous:   
        return redirect('app:no-access')
    #permision ----end-----
    profile_obj = request.user.profile
    #permission ---start---
    if not profile_obj.is_organiser:   
        return redirect('app:no-access')
    #permision ----end-----
    form = SignupForm(instance=request.user)
    org_form = OrganizerForm(instance=request.user.profile.orgprofile)
    if request.method == "POST":
        form = SignupForm(request.POST,instance=request.user)
        org_form = OrganizerForm(request.POST,request.FILES,instance=request.user.profile.orgprofile)
        if form.is_valid() and org_form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.set_password(user_obj.password)
            user_obj.save()
            login(request,user_obj)
            org_obj = org_form.save(commit=False)
            org_obj.user = user_obj
            org_obj.save()
            messages.success(request, 'Your profile has been updated, %s!' %(org_obj.org_name))
            return redirect('app:dashboard')

    context = {                             
        "form": form,
        "org_form": org_form
    }
    return render(request,'update_organiser.html',context)

    
def event_delete(request,event_slug):
    event = Event.objects.get(slug=event_slug)
    #permission ---start---
    if request.user != event.owner:  
        return redirect('app:no-access')
    #permision ----end-----
    if event.datetime < timezone.now():   
        return redirect ('app:no-access')
    #permision ----end-----
    if event.seats != event.available_seats:
        reserved = event.seats - event.available_seats
        messages.warning (request, "%s seats already booked,you can only delete an event if no bookings are made!"%(reserved))
        return redirect ('app:detail', event_slug)
    event.delete()
    messages.warning (request, "event deleted successfully")
    return redirect('app:list')


def booking_delete(request,booking_id):
    user_slug = request.user.profile.userprofile.slug
    booking = Booking.objects.get(id=booking_id)
    booking_time = booking.event.datetime
    days_dif = booking_time - timezone.now()
    #permission ---start---
    print(days_dif.total_seconds())
    if days_dif.total_seconds()/3600 < 3:  
        messages.warning (request, "cannot delete booking starting after 3 hours or less")
        return redirect('app:user-profile',user_slug)
    #permision ----end-----
    else:
        booking.event.available_seats += booking.desired_seats
        booking.event.save()
        booking.delete()
        messages.warning (request, "booking deleted successfully")
        return redirect('app:user-profile',user_slug)


def user_profile(request,user_slug):
    user_obj = UserProfile.objects.get(slug=user_slug)
    profile_obj = request.user.profile
    followers_count = OrgProfile.objects.filter(followers=user_obj).count()
    followers_list = OrgProfile.objects.filter(followers=user_obj)
    past_events = request.user.attended.filter(event__datetime__lt=timezone.now())
    upcoming_events = request.user.attended.filter(event__datetime__gte=timezone.now())
    context = {
     "user_obj":user_obj,
     "followers":followers_count,
     "followers_list": followers_list,
     "past_events":past_events,
     "upcoming_events":upcoming_events
    }
    return render(request,'user_profile.html',context)


def org_profile(request,org_slug):

    organiser_obj = OrgProfile.objects.get(slug=org_slug)
    profile_obj = request.user.profile
    following = organiser_obj.followers.filter(profile=profile_obj).exists()
    followers_count = UserProfile.objects.filter(orgprofile=organiser_obj).count()
    followers_list = UserProfile.objects.filter(orgprofile=organiser_obj)
    print(request.user)
    upcoming_events = Event.objects.filter(datetime__gte=datetime.now(),owner=organiser_obj.profile.user)


    context = {
     "organiser":organiser_obj,
     "following":following,
     "followers":followers_count,
     "followers_list": followers_list,
     "upcoming_events":upcoming_events
    }
    return render(request,'org_profile.html',context)



def followers_list(request,org_slug):
    organiser_obj = OrgProfile.objects.get(slug=org_slug)
    followers_list = UserProfile.objects.filter(orgprofile=organiser_obj)
    context = {
     "followers_list": followers_list
    }
    return render(request,'followers_list.html',context)


def following_list(request,user_slug):
    user_obj = UserProfile.objects.get(slug=user_slug)
    following_list = OrgProfile.objects.filter(followers=user_obj)
    context = {
     "following_list": following_list
    }
    return render(request,'following_list.html',context)


def org_follow(request,org_slug):
    organiser_obj = OrgProfile.objects.get(slug=org_slug)
    #permission ---start--- 
    if request.user.is_anonymous:   
        messages.success (request, "You must sign in to be able to follow organizers!")
    #permision ----end-----
    else:
        user_obj = request.user.profile.userprofile
        profile_obj = request.user.profile
        organiser_obj.followers.add(user_obj)
        #print(user_obj.orgprofile_set.all())
        following = organiser_obj.followers.filter(profile=profile_obj).exists()
        return redirect('app:org-profile',org_slug)

def org_unfollow(request,org_slug):
    organiser_obj = OrgProfile.objects.get(slug=org_slug)
    user_obj = request.user.profile.userprofile 
    profile_obj = request.user.profile
    organiser_obj.followers.remove(user_obj)
    #print(user_obj.orgprofile_set.all())
    following = organiser_obj.followers.filter(profile=profile_obj).exists()
    return redirect('app:org-profile',org_slug)





