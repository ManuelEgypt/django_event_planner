from rest_framework.permissions import BasePermission

from datetime import date





class IsBookingOwner(BasePermission):

	message = "You must be the owner of this booking"
	def has_object_permission(self, request, view, obj):

		if (request.user == obj.user) or (obj.user.profile.is_organiser):

			return True

		else:

			return False





class IsChangable(BasePermission):

	message = "Booking cannot be cancelled or modified"
	def has_object_permission(self, request, view, obj):

		days_left = (obj.date - date.today()).days

		if  days_left > 3:

			return True

		else:

			return False