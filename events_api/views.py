from rest_framework.permissions import IsAuthenticated

from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView

from rest_framework.filters import SearchFilter, OrderingFilter

from datetime import datetime



from events.models import Event,Booking

from .serializers import 

from .permissions import IsBookingOwner, IsChangable





class EventsList(ListAPIView):

	queryset = Event.objects.all()

	serializer_class = EventSerializer

	filter_backends = [SearchFilter, OrderingFilter]

	search_fields = ['destination']





class BookingsList(ListAPIView):

	serializer_class = BookingSerializer

	permission_classes = [IsAuthenticated]



	def get_queryset(self):

		return Booking.objects.filter(user=self.request.user, date__gte=datetime.today())





class BookingDetails(RetrieveAPIView):

	queryset = Booking.objects.all()

	serializer_class = BookingDetailsSerializer

	lookup_field = 'id'

	lookup_url_kwarg = 'booking_id'

	permission_classes = [IsAuthenticated, IsBookingOwner]




class BookEvent(CreateAPIView):

	serializer_class = AdminUpdateBookingSerializer

	permission_classes = [IsAuthenticated]



	def perform_create(self, serializer):

		serializer.save(user=self.request.user, event_slug=self.kwargs['event_slug'])





class Register(CreateAPIView):

	serializer_class = RegisterSerializer





class ProfileDetails(RetrieveAPIView):

	serializer_class = ProfileSerializer

	permission_classes = [IsAuthenticated]

	

	def get_object(self):

		return self.request.user.profile






