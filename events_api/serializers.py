from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from datetime import date
from events.models import Event,Booking,Profile,OrgProfile,UserProfile 





class EventSerializer(serializers.ModelSerializer):
	owner = serializers.SlugRelatedField(

		 read_only= True, slug_field = 'username')

	class Meta:
		model = Event
		fields = ['name', 'seats', 'date', 'time','location','description','available_seats','owner']


class UserSerializer(serializers.ModelSerializer):
	username = serializers.CharField(max_length=30)
	password = serializers.CharField(max_length=30)
	full_name = serializers.CharField(max_length=50)
	email = serializers.EmailField()




class OrgSignupSerializer(serializers.ModelSerializer):
	username = serializers.CharField(max_length=30)
	password = serializers.CharField(max_length=30)
	org_name = serializers.CharField(max_length=50)
	email = serializers.EmailField()
	org_description = serializers.CharField(max_length=30)



class BookingSerializer(serializers.ModelSerializer):

	event = serializers.SlugRelatedField(

		 read_only= True, slug_field = 'name')

	class Meta:

		model = Booking

		fields = ['event', 'user', 'desired_seats']




class UserBookingSerializer(serializers.ModelSerializer):

	user = serializers.SlugRelatedField(

		 read_only= True, slug_field = 'username')


	class Meta:

		model = Booking

		fields = ['user']




class OrganizerSerializer(serializers.ModelSerializer):

	class Meta:

		model = OrgProfile

		fields = ['org_name', 'org_description']




class BookEventSerializer(serializers.ModelSerializer):

	event = serializers.SlugRelatedField(

		 read_only= True, slug_field = 'name')
		 	
	class Meta:

		model = Booking

		fields = ['event', 'desired_seats']





class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:

        model = User

        fields = ['username', 'password', 'first_name', 'last_name']





    def create(self, validated_data):

        username = validated_data['username']

        password = validated_data['password']

        new_user = User(username=username, first_name=first_name, last_name=last_name)

        new_user.set_password(password)

        new_user.save()

        return validated_data




class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['is_organiser']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['full_name','profile']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)
    userprofile = UserProfileSerializer(required=True)
    class Meta:
        model = User
        fields = ['username', 'password','profile','userprofile']

    def create(self, validated_data):

        # create user 
        user = User.objects.create(
            username = validated_data['username'],
            password = validated_data['password']
            # etc ...
        )

        profile_data = validated_data.pop('profile')
        # create profile
        profile = Profile.objects.create(
            user = user,
            is_organiser = profile_data['is_organiser']   
            # etc...
        )


        return user 



# class ProfileCreateSerializer(serializers.ModelSerializer):
#    username = serializers.CharField(source='user.username',max_length=30)

#    class Meta:
#        model = Profile
#        fields = [
#        'username',
#        'is_organiser',
#        ]

#    def create (self, validated_data):
#     user = get_user_model().objects.create(username=validated_data['username'])
#     user.set_password(User.objects.make_random_password())
#     user.save()

#     profile = Profile.objects.create(user = user)

#     return profile





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


