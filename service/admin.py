from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django import forms


# Define Reminder inline admin
class ReminderInline(admin.TabularInline):
    model = models.Reminder


class BookingInline(admin.TabularInline):
    model = models.Booking


# Extend the User admin with inline reminders
class UserAdmin(BaseUserAdmin):
    inlines = [ReminderInline, BookingInline]


# Unregister the default User admin
admin.site.unregister(User)
# Register User with custom admin
admin.site.register(User, UserAdmin)


# Register other models
@admin.register(models.Hotel)
class BeautyHotel(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "description",
        "contact_email",
        "contact_phone",
        "facebook",
        "instagram",
        "twitter",
    ]


class RoomTypeAdminForm(forms.ModelForm):
    class Meta:
        model = models.RoomType
        fields = "__all__"

    amenities = forms.ModelMultipleChoiceField(
        queryset=models.Amenity.objects.all(), widget=forms.CheckboxSelectMultiple
    )


class RoomTypeAdmin(admin.ModelAdmin):
    form = RoomTypeAdminForm


admin.site.register(models.RoomType, RoomTypeAdmin)


@admin.register(models.Amenity)
class BeautyAmenity(admin.ModelAdmin):
    list_display = ["name", "description", "is_available", "icon"]


# @admin.register(models.RoomType)
# class BeautyRoomtype(admin.ModelAdmin):
#     list_display = ["id", "name", "description", "capacity", "price"]


@admin.register(models.Room)
class BeautyRoom(admin.ModelAdmin):
    list_display = ["id", "number", "room_type", "hotel"]


@admin.register(models.RoomAvailability)
class BeautyRoomavailability(admin.ModelAdmin):
    list_display = ["id", "room", "start_date", "end_date"]


@admin.register(models.Booking)
class BeautyBooking(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "room",
        "check_in_date",
        "check_out_date",
        "total_price",
        "payment_status",
    ]


@admin.register(models.Review)
class BeautyReview(admin.ModelAdmin):
    list_display = ["id", "user", "room", "rating", "review_text", "date"]


@admin.register(models.Event)
class BeautyEvent(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "date",
        "start_time",
        "end_time",
        "location",
        "organiser",
    ]


@admin.register(models.Restaurant)
class BeautyEvent(admin.ModelAdmin):
    list_display = ["id", "name", "description", "image"]


@admin.register(models.Wellness)
class BeautyWellness(admin.ModelAdmin):
    list_display = ["id", "name", "description"]


# @admin.register(models.Reminder)
# class BeautyReminder(admin.ModelAdmin):
#     list_display = ["id", "user", "event", "booking", "reminder_time", "is_seen"]
@admin.register(models.Reminder)
class BeautyReminder(admin.ModelAdmin):
    list_display = ["user", "event", "booking", "reminder_time", "is_seen"]


@admin.register(models.MPesaTransaction)
class BeautyMpesaTransaction(admin.ModelAdmin):
    list_display = [
        "transaction_id",
        "booking",
        "amount",
        "phone_number",
        "status",
        "created_at",
    ]


@admin.register(models.PhoneNumber)
class BeautyPhoneNumber(admin.ModelAdmin):
    list_display = ["phone_number"]
