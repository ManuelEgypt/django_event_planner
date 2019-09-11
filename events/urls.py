from django.urls import path
from . import views 


app_name = 'events'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('404/', views.no_access, name='no-access'),
    path('signup/', views.signup, name='signup'),   
    path('signup/organisation', views.org_signup, name='org-signup'),   
    path('signin/', views.signin, name='signin'),   
    path('signout/', views.signout, name='signout'),  
    path('list/', views.event_list, name='list'),   
    path('dashboard/', views.dashboard, name='dashboard'),   
    path('organisation/profile/<slug:org_slug>', views.org_profile, name='org-profile'),   
    path('user/profile/<slug:user_slug>', views.user_profile, name='user-profile'),   
    path('followers/<slug:org_slug>', views.followers_list, name='followers'),   
    path('following/<slug:user_slug>', views.following_list, name='following'),   
    path('follow/<slug:org_slug>', views.org_follow, name='org-follow'),   
    path('unfollow/<slug:org_slug>', views.org_unfollow, name='org-unfollow'),   
    path('detail/<slug:event_slug>', views.event_detail, name='detail'),   
    path('create/', views.event_create, name='create'),   
    path('update/<slug:event_slug>', views.event_update, name='update'),	
    path('user/update', views.update_user, name='update-user'),    
    path('organiser/update', views.update_organiser, name='update-organiser'),    
    path('delete/<slug:event_slug>', views.event_delete, name='delete'),
    path('booking/delete/<int:booking_id>', views.booking_delete, name='booking-delete'),
    path('book/<slug:event_slug>', views.booking_create, name='booking-create'),
    path('email/',views.email,name="email")
]

