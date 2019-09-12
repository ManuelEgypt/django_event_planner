from django.urls import path
from . import views 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'api'

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='login'),
    # path('signup/', views.signup, name='signup'),
    # path('signin/', views.signin, name='signin'),
    # path('signout/', views.signout, name='signout'),   
    path('list/', views.EventsList.as_view(), name='list'), 
    path('org/list/<int:owner_id>', views.OrgEventsList.as_view(), name='org-list'),
    path('booking/update/<int:booking_id>', views.UpdateBooking.as_view(), name='booking-update'),
    path('event/attending/<int:event_id>', views.UserBookingsList.as_view(), name='events-attending'),
    path('register/', views.UserList.as_view(), name='register-user'),

    # path('dashboard/', views.dashboard, name='dashboard'), 
    # path('detail/<slug:event_slug>', views.event_detail, name='detail'),
    # path('create/', views.event_create, name='create'),
    # path('update/<slug:event_slug>', views.event_update, name='update'),
    # path('delete/<slug:event_slug>', views.event_delete, name='delete'),
    path('book/<int:event_id>', views.BookEvent.as_view(), name='booking-create'),
]