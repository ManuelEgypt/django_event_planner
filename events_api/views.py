from rest_framework.permissions import IsAuthenticated

from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User


from events.models import Event,Booking,Profile

from .serializers import EventSerializer,BookingSerializer,OrganizerSerializer,BookEventSerializer,RegisterSerializer,UserBookingSerializer,UserSerializer,UserProfileSerializer
from .permissions import IsBookingOwner, IsChangable





class EventsList(ListAPIView):
	serializer_class = EventSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['name']

	def get_queryset(self):
		return Event.objects.filter(date__gte=datetime.today())



class OrgEventsList(ListAPIView):
	serializer_class = EventSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['name']

	def get_queryset(self):
		return Event.objects.filter(owner_id=self.kwargs['owner_id'])



class UserEventsList(ListAPIView):
	serializer_class = BookEventSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['name']
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		return Booking.objects.filter(user=self.request.user)


class UpdateBooking(RetrieveUpdateAPIView): 
	serializer_class = BookEventSerializer
	queryset = Booking.objects.all()
	lookup_field = 'id'
	lookup_url_kwarg = 'booking_id'
	permission_classes = [IsAuthenticated,IsBookingOwner]


class BookingsList(ListAPIView):

	serializer_class = BookingSerializer

	permission_classes = [IsAuthenticated]



	def get_queryset(self):
		return Booking.objects.filter(user=self.request.user, date__gte=datetime.today())





class BookingsList(ListAPIView):

	serializer_class = OrganizerSerializer

	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		return OrgProfile.objects.filter(user=self.request.user, date__gte=datetime.today())



class UserBookingsList(ListAPIView):

	serializer_class = UserBookingSerializer

	permission_classes = [IsAuthenticated]


	def get_queryset(self):
		return Booking.objects.filter(event_id=self.kwargs['event_id'])



class BookEvent(CreateAPIView):

	serializer_class = BookEventSerializer

	permission_classes = [IsAuthenticated]


	def perform_create(self, serializer):
		serializer.save(user=self.request.user, event_id=self.kwargs['event_id'])



class UserList(CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BookingsList(ListAPIView):

	serializer_class = UserProfileSerializer

	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user.profile)


# class ProfileCreateAPIView(CreateAPIView):
#     model = Profile
#     serializer_class = ProfileCreateSerializer

#     def post(self, request, *args, **kwargs):
#         validated_data = {
#             'username': request.data.get('username', None),
#             'is_organiser': request.data.get('is_organiser', None),

#         }

#         serializer = ProfileCreateSerializer(data=validated_data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class StatesDetailSerializer(CreateAPIView):

# 	serializer_class = StatesDetailSerializer












