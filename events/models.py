from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from datetime import datetime
from django.utils import timezone

class Event(models.Model):
	name = models.CharField(max_length = 30)
	seats = models.IntegerField()
	date = models.DateField(null=True)		# redundant
	datetime = models.DateTimeField(null=True)
	time = models.TimeField(null=True)		# redudant
	location = models.CharField(max_length = 30)
	description = models.TextField()
	available_seats = models.IntegerField()		# redundant - should be calculated in a model method
	image = models.ImageField(null = True, blank = True)  
	owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name='events')
	slug = models.SlugField(unique=True,blank=True)

	def get_absolute_url(self):
		return reverse('app:detail', kwargs={'event_slug':self.slug})

	def __str__(self):
		return self.name

	def is_full(self):
		if self.available_seats == 0:
			return True
		else:
			return False

	def is_past(self):
		if self.datetime < timezone.now():
			return True
		else:
			return False





# DRY = Don't Repeat Yourself
# ModelName parameter
def create_slug(instance, new_slug=None):
	slug = slugify(instance.name)
	if new_slug is not None:
		slug = new_slug
	qs = Event.objects.filter(slug=slug)
	if qs.exists():
		try:
			int(slug[-1])
			if "-" in slug:
				slug_list = slug.split("-")
				new_slug = "%s%s" % (slug[:-len(slug_list[-1])], int(slug_list[-1]) + 1)
			else:
				new_slug = "%s-1" % (slug)
		except:
			new_slug = "%s-1" % (slug)
		return create_slug(instance, new_slug=new_slug)
	return slug

# More meaningful name
@receiver(pre_save, sender=Event)
def generate_slug(instance, *args, **kwargs):
	if not instance.slug:
		instance.slug=create_slug(instance)


class Booking(models.Model):
	event = models.ForeignKey(Event, on_delete = models.CASCADE, related_name='bookings')
	user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='attended')
	desired_seats = models.IntegerField()

	def book_seat(self):
		if self.event.available_seats >= self.desired_seats:
			self.event.available_seats -= self.desired_seats
			return True
		else:
			return False

# Redundant
class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	is_organiser = models.BooleanField(default=False)


class UserProfile(models.Model):
	profile = models.OneToOneField(Profile,on_delete=models.CASCADE)
	full_name = models.CharField(max_length = 50)	# redundant
	profile_pic = models.ImageField(null = True, blank = True)	# naming
	slug = models.SlugField(unique=True,blank=True)


def create_slug3(instance, new_slug=None):
	slug = slugify(instance.full_name)
	if new_slug is not None:
		slug = new_slug
	qs = UserProfile.objects.filter(slug=slug)
	if qs.exists():
		try:
			int(slug[-1])
			if "-" in slug:
				slug_list = slug.split("-")
				new_slug = "%s%s" % (slug[:-len(slug_list[-1])], int(slug_list[-1]) + 1)
			else:
				new_slug = "%s-1" % (slug)
		except:
			new_slug = "%s-1" % (slug)
		return create_slug3(instance, new_slug=new_slug)
	return slug

# More meaningful name
@receiver(pre_save, sender=UserProfile)
def generate_slug3(instance, *args, **kwargs):
	if not instance.slug:
		instance.slug=create_slug3(instance)



class OrgProfile(models.Model):
	profile = models.OneToOneField(Profile,on_delete=models.CASCADE)
	org_name = models.CharField(max_length = 30)	# naming
	org_description = models.TextField()	# naming
	org_logo = models.ImageField(null = True, blank = True)	# naming
	slug = models.SlugField(unique=True,blank=True)
	followers = models.ManyToManyField(UserProfile)



def create_slug2(instance, new_slug=None):
	slug = slugify(instance.org_name)
	if new_slug is not None:
		slug = new_slug
	qs = OrgProfile.objects.filter(slug=slug)
	if qs.exists():
		try:
			int(slug[-1])
			if "-" in slug:
				slug_list = slug.split("-")
				new_slug = "%s%s" % (slug[:-len(slug_list[-1])], int(slug_list[-1]) + 1)
			else:
				new_slug = "%s-1" % (slug)
		except:
			new_slug = "%s-1" % (slug)
		return create_slug2(instance, new_slug=new_slug)
	return slug

# More meaningful name
@receiver(pre_save, sender=OrgProfile)
def generate_slug2(instance, *args, **kwargs):
	if not instance.slug:
		instance.slug=create_slug2(instance)






