from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    facebook = models.CharField(max_length=50)
    instagram = models.CharField(max_length=50)
    twitter = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Amenity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(
        blank=True, null=True, default=None
    )  # Description of the amenity
    is_available = models.BooleanField(default=True)  # Whether the amenity is active
    icon = models.ImageField(
        upload_to="amenities/icons/", blank=True, null=True
    )  # Icon image for the amenity

    def __str__(self):
        return self.name


class RoomType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amenities = models.ManyToManyField(Amenity)
    image = models.ImageField(upload_to="roomtype_images/", default=None)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("service:rooms", args=[self.id])


class Room(models.Model):
    number = models.CharField(max_length=10)
    room_type = models.ForeignKey(
        RoomType, on_delete=models.CASCADE
    )  # each room belongs to exactly ONE type
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    beds = models.IntegerField(default=None)
    image = models.ImageField(upload_to="room_images/", default=None)

    def __str__(self):
        return f"{self.room_type.name} - {self.number}"

    def is_available_on(self, date):
        return not self.availabilities.filter(
            start_date__lte=date, end_date__gte=date
        ).exists()

    def is_available_for_dates(self, start_date, end_date):
        return not self.availabilities.filter(
            models.Q(start_date__lte=end_date) & models.Q(end_date__gte=start_date)
        ).exists()


class RoomAvailability(models.Model):
    room = models.ForeignKey(
        Room, related_name="availabilities", on_delete=models.CASCADE
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Room {self.room.number} not available from {self.start_date} to {self.end_date}"

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gt=models.F("start_date")),
                name="end_date_after_start_date",
            )
        ]

    @property
    def is_currently_unavailable(self):
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date


class Booking(models.Model):
    class status(models.TextChoices):
        pending = "pending"
        paid = "paid"
        not_payed = "payment not made"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=status.choices)

    def __str__(self):
        return f"{self.user.username} - {self.room.room_type.name} - {self.check_in_date} to {self.check_out_date}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.room.room_type.name} - {self.date}"


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to="event_images/")
    organiser = models.CharField(max_length=80)
    entry = models.CharField(max_length=200, default="to be communicated")

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("service:event_info", args=[self.name])


class Restaurant(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to="restaurant_images/")
    about = models.TextField(null=True)
    opening = models.TimeField(default=None, null=True)
    closing = models.TimeField(default=None, null=True)

    def get_absolute_url(self):
        return reverse("service:dish_r", args=[self.name])


class Wellness(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    about = models.TextField()
    is_available = models.BooleanField(default=True)
    opening = models.TimeField()
    closing = models.TimeField()
    image = models.ImageField(upload_to="wellness_images/")

    def get_absolute_url(self):
        return reverse("service:dish_w", args=[self.name])


class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, null=True, blank=True
    )
    reminder_time = models.DateTimeField()
    is_seen = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"Reminder for {self.event} at {self.reminder_time}"
            if self.event
            else f"Reminder for booking at {self.reminder_time}"
        )


class PhoneNumber(models.Model):
    users = models.ManyToManyField(User, related_name="phone_numbers")
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.phone_number


class MPesaTransaction(models.Model):
    class status(models.TextChoices):
        pending = "pending"
        paid = "paid"
        not_payed = "payment not made"

    transaction_id = models.CharField(max_length=100)
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name="mpesa_transactions"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.ForeignKey(
        PhoneNumber, on_delete=models.SET_NULL, null=True, blank=True
    )
    status = models.CharField(max_length=30, choices=status.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.transaction_id
