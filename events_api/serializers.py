from rest_framework import serializers

from django.contrib.auth.models import User

from datetime import date

from events.models import Event, Booking 





class EventSerializer(serializers.ModelSerializer):

	class Meta:

		model = Event

		fields = ['destination', 'time', 'price', 'id']



class BookingSerializer(serializers.ModelSerializer):

	event = serializers.SlugRelatedField(

		 read_only= True, slug_field = 'destination')

	class Meta:

		model = Booking

		fields = ['event', 'date', 'id']





class BookingDetailsSerializer(serializers.ModelSerializer):

	event = EventSerializer()

	total = serializers.SerializerMethodField()



	class Meta:

		model = Booking

		fields = ['event', 'date', 'passengers', 'id', 'total']



	def get_total(self, obj):

		return obj.passengers * obj.event.price



class AdminUpdateBookingSerializer(serializers.ModelSerializer):

	class Meta:

		model = Booking

		fields = ['date', 'passengers']





class UpdateBookingSerializer(serializers.ModelSerializer):

	class Meta:

		model = Booking

		fields = ['passengers']



class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:

        model = User

        fields = ['username', 'password', 'first_name', 'last_name']



    def create(self, validated_data):

        username = validated_data['username']

        password = validated_data['password']

        first_name = validated_data['first_name']

        last_name = validated_data['last_name']

        new_user = User(username=username, first_name=first_name, last_name=last_name)

        new_user.set_password(password)

        new_user.save()

        return validated_data



class UserSerializer(serializers.ModelSerializer):

	class Meta:

		model = User

		fields = ['first_name', 'last_name']





# class ProfileSerializer(serializers.ModelSerializer):

# 	user = UserSerializer()

# 	past_bookings = serializers.SerializerMethodField()

# 	tier = serializers.SerializerMethodField()



# 	class Meta:

# 		model = Profile

# 		fields = ['user', 'miles', 'past_bookings', 'tier']



# 	def get_past_bookings(self, obj):

# 		booking = Booking.objects.filter(user=obj.user, date__lt=date.today())

# 		return BookingSerializer(booking, many=True).data


