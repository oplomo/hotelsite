from django import forms
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from .models import RoomType


class loginform(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords don't match.")
        return cd["password2"]

    def clean_email(self):
        data = self.cleaned_data["email"]
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("Email already in use.")
        return data


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username"]

        def clean_username(self):
            name = self.cleaned_data["username"]
            email = self.cleaned_data["email"]
            if User.objects.filter(username=name).exists():
                raise forms.ValidationError("a user with this user name already exist")
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Email already in use.")
            return name, email


class ReminderForm(forms.Form):
    reminder_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )

    def clean_reminder_time(self):
        reminder_time = self.cleaned_data["reminder_time"]
        if reminder_time <= datetime.now():
            raise forms.ValidationError("Reminder time must be in the future.")
        return reminder_time


# forms.py


class DateRangeForm(forms.Form):
    today = timezone.now().date()
    tomorrow = today + timezone.timedelta(days=1)

    start_date = forms.DateField(
        widget=forms.TextInput(attrs={"type": "date", "value": today}),
        label="Start Date",
        initial=today,
    )
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={"type": "date", "value": tomorrow}),
        label="End Date",
        initial=tomorrow,
    )

    ROOM_TYPE_CHOICES = [("", "All")] + [
        (room_type.id, room_type.name) for room_type in RoomType.objects.all()
    ]

    room_type = forms.ChoiceField(
        choices=ROOM_TYPE_CHOICES, label="Room Type", required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        # Ensure start date is not in the past
        if start_date < self.today:
            raise forms.ValidationError("Start date cannot be in the past.")

        # Ensure end date is greater than start date
        if end_date <= start_date:
            raise forms.ValidationError("End date must be greater than start date.")


class RoomAvailabilityForm(forms.Form):
    today = timezone.now().date()

    start_date = forms.DateField(
        label="Start Date",
        widget=forms.DateInput(attrs={"type": "date", "placeholder": today}),
        initial=today,
    )
    duration = forms.IntegerField(
        label="Duration of Stay (in days)",
        initial=1,
        min_value=1,
        widget=forms.NumberInput(attrs={"placeholder": 1}),
    )

    def clean_start_date(self):
        start_date = self.cleaned_data.get("start_date")

        # Ensure start date is not in the past
        if start_date < timezone.now().date():
            raise forms.ValidationError("Start date cannot be in the past.")

        return start_date

    def clean_duration(self):
        duration = self.cleaned_data.get("duration")

        # Ensure duration is a positive integer
        if duration < 1:
            raise forms.ValidationError("Duration must be a positive integer.")

        return duration


class EmailForm(forms.Form):
    email_content = forms.CharField(widget=forms.Textarea, label="Compose Email:")
    specific_user_email = forms.EmailField(
        required=False, label="Send to specific user:"
    )
    send_to_all = forms.BooleanField(required=False, label="Or send to all users")


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Your Name")
    email = forms.EmailField(required=True, label="Your Email")
    subject = forms.CharField(max_length=200, required=True, label="Subject")
    message = forms.CharField(widget=forms.Textarea, required=True, label="Message")
