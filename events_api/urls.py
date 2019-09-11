from django.urls import path
from . import views 

app_name = 'events'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),   
    path('list/', views.event_list, name='list'), 
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('detail/<slug:event_slug>', views.event_detail, name='detail'),
    path('create/', views.event_create, name='create'),
    path('update/<slug:event_slug>', views.event_update, name='update'),
    path('delete/<slug:event_slug>', views.event_delete, name='delete'),
    path('book/<slug:event_slug>', views.booking_create, name='booking-create'),
]