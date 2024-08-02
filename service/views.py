# celery -A hotel  worker --pool=solo -l info


from django.shortcuts import render, get_object_or_404, redirect
from .models import (
    Hotel,
    Restaurant,
    Wellness,
    Event,
    Reminder,
    RoomType,
    Room,
    Booking,
    RoomAvailability,
    Review,
    MPesaTransaction,
    PhoneNumber,
)
from django.views.generic import ListView
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import (
    loginform,
    UserRegistrationForm,
    UserEditForm,
    ReminderForm,
    DateRangeForm,
    RoomAvailabilityForm,
    ContactForm,
)
from .tasks import send_reminder_email, send_registration_email, send_booking_email
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q, BooleanField, Value, OuterRef, Exists

# GurstEditForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import random
from django.contrib import messages
from datetime import timedelta
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from cart.forms import CartAddRoomForm
from cart.cart import Cart


from django.http import JsonResponse
from django_daraja.mpesa.core import MpesaClient
from django.db import transaction


details = Hotel.objects.all()


class Home(ListView):
    context_object_name = "details"
    template_name = "service/res/index.html"

    def get_queryset(self):
        return Hotel.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset1 = Hotel.objects.all()  # queryset for Hotel
        queryset2 = Restaurant.objects.all()
        queryset3 = Wellness.objects.all()
        queryset4 = Event.objects.all()
        queryset5 = RoomType.objects.all()
        form = DateRangeForm()

        context["hotel"] = queryset1
        context["restaurant"] = queryset2[:3]
        context["act"] = queryset3[:3]
        context["event"] = queryset4
        context["rtype"] = queryset5
        context["form"] = form

        return context


class Restaurant_page(ListView):
    context_object_name = "restaurant"
    template_name = "service/res/restaurant.html"

    def get_queryset(self):
        return Restaurant.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset1 = Hotel.objects.all()  # queryset for Hotel
        queryset2 = Restaurant.objects.all()

        context["hotel"] = queryset1
        context["restaurant"] = queryset2

        return context


def dish_r(request, name):
    dish = get_object_or_404(Restaurant, name=name)
    hotel = get_object_or_404(Hotel)

    return render(
        request,
        "service/res/dish.html",
        {"dish": dish, "hotel": hotel, "name": "restaurant"},
    )


def dish_w(request, name):
    dish = get_object_or_404(Wellness, name=name)
    hotel = get_object_or_404(Hotel)

    return render(
        request,
        "service/res/dish.html",
        {"hotel": hotel, "dish": dish, "name": "wellness"},
    )


def about(request):
    hotel = Hotel.objects.get(pk=1)
    return render(request, "service/res/about.html", {"hotel": hotel})


def gallery(request):
    hotel = Hotel.objects.all()
    return render(request, "service/res/gallery.html", {"hotel": hotel})


def wellness(request):
    activity = Wellness.objects.all()
    act = activity[:3]
    return render(
        request, "service/res/wellness.html", {"act": act, "activity": activity}
    )


def Roomtype(request):
    rms = RoomType.objects.all()
    return render(request, "service/res/roomtypes.html", {"room": rms})


def rooms(request, id):
    # room = Room.objects.filter(room_type=id)
    room_type = get_object_or_404(RoomType.objects.prefetch_related("amenities"), id=id)
    today = timezone.now().date()
    hotel = get_object_or_404(Hotel)

    form = RoomAvailabilityForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        start_date = form.cleaned_data["start_date"]
        duration = form.cleaned_data["duration"]
        end_date = start_date + timedelta(days=duration - 1)

        # Filter available rooms based on the selected date range
        available_rooms = Room.objects.filter(
            Q(room_type=id)
            & (
                ~Q(
                    availabilities__start_date__lte=end_date,
                    availabilities__end_date__gte=start_date,
                )
                | ~Q(availabilities__isnull=False)
            )
        ).distinct()

        all_rooms = Room.objects.filter(room_type=id).annotate(
            is_available=Exists(available_rooms.filter(pk=OuterRef("pk")))
        )

        return render(
            request,
            "service/res/rooms.html",
            {
                "hotel": hotel,
                "amn": room_type,
                "name": "roomtype",
                "room": all_rooms,
                "start_date": start_date,
                "duration": duration,
                "form": form,
            },
        )

    start_date = form.initial.get("start_date", today)
    duration = form.initial.get("duration", 1)
    end_date = start_date + timedelta(days=duration - 1)
    room = Room.objects.filter(room_type=id)

    available_rooms = Room.objects.filter(
        Q(room_type=id)
        & (
            ~Q(
                availabilities__start_date__lte=end_date,
                availabilities__end_date__gte=start_date,
            )
            | ~Q(availabilities__isnull=False)
        )
    ).distinct()
    all_rooms = Room.objects.filter(room_type=id).annotate(
        is_available=Exists(available_rooms.filter(pk=OuterRef("pk")))
    )

    return render(
        request,
        "service/res/rooms.html",
        {
            "hotel": hotel,
            "amn": room_type,
            "name": "roomtype",
            "room": all_rooms,
            "today": today,
            "start_date": start_date,
            "duration": duration,
            "form": form,
        },
    )


@transaction.atomic
def account(request):
    hotel = Hotel.objects.all()
    current_user = request.user
    user_reminders = Reminder.objects.filter(user=current_user)
    user_booking = Booking.objects.filter(user=current_user)
    cart = Cart(request)
    bkd_room = {}
    hot = get_object_or_404(Hotel, pk=1)
    hotel_name = hot.name
    if request.method == "POST":

        phone_number = request.POST.get("phone_number")
        am = request.POST.get("amount")
        amn = float(am)
        amount = round(amn)
        account_reference = f"{hotel_name}"
        transaction_desc = f"Payment for booking"

        mpesa_client = MpesaClient()

        try:
            response = mpesa_client.stk_push(
                phone_number,
                amount,
                account_reference,
                transaction_desc,
                callback_url="https://darajambili.herokuapp.com/express-payment",
                # callback_url=settings.MPESA_CALLBACK_URL,
            )

        except Exception as e:
            return f"Mpesa payment initiation failed: {str(e)}"

        phone_number_instance, created = PhoneNumber.objects.get_or_create(
            phone_number=phone_number
        )

        for room in cart:
            current_b = Booking.objects.create(
                user=current_user,
                room=room["room"],
                check_in_date=room["start_date"],
                check_out_date=room["end_date"],
                total_price=room["total_price"],
                payment_status="paid",
            )
            booking_instance = current_b
            MPesaTransaction.objects.create(
                transaction_id=response.checkout_request_id,
                booking=booking_instance,
                amount=amount,
                phone_number=phone_number_instance,
                status="Pending",
            )

            RoomAvailability.objects.create(
                room=room["room"],
                start_date=room["start_date"],
                end_date=room["end_date"],
            )
            room_name = room["room"]
            bkd_room[room_name] = {
                "start_date": room["start_date"],
                "end_date": room["end_date"],
            }
        rooms_info = "; ".join(
            [
                f"{room}: {details['start_date']} - {details['end_date']}"
                for room, details in bkd_room.items()
            ]
        )
        cart.clear()

        subject = "SUCCESFUL ROOM BOOKING"
        message = (
            f"JAMBO! {current_user.username},"
            f"Your booking with {hotel_name} has been successfull. "
            f"Rooms booked:\n{rooms_info}"
            f"Experience luxury at its best. WELCOME!\n\n"
        )
        from_email = settings.EMAIL_HOST_USER
        to_email = [current_user.email]

        send_booking_email.delay(
            subject,
            message,
            from_email,
            to_email,
        )

        # response_des = response.response_description
        # response_data = {"response_des": response_des}
        # return JsonResponse(response_data, safe=False)
    return render(
        request,
        "service/res/account.html",
        {"rmb": user_reminders, "hotel": hotel, "book": user_booking},
    )


def register(request):

    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            rand = random.randint(1000, 10000)
            first_name = user_form.cleaned_data["first_name"]
            username = first_name + str(rand)
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.username = username
            new_user.set_password(user_form.cleaned_data["password"])

            # Save the User object
            new_user.save()

            subject = "SUCCESFUL REGISTRATION"
            message = f"your account with ST.RAYAN HOTEL has sucessfully been created.your username is {username} always use it to login. experience luxury at it's best. WELCOME!"
            from_email = settings.EMAIL_HOST_USER
            to_email = [
                user_form.cleaned_data["email"]
            ]  # Assuming user is the recipient

            send_registration_email.delay(
                subject,
                message,
                from_email,
                to_email,
            )
            form = AuthenticationForm()
            return render(
                request,
                "service/res/registration_done.html",
                {"new_user": new_user, "name": username, "form": form},
            )
    else:
        user_form = UserRegistrationForm()
    return render(request, "service/res/registration.html", {"user_form": user_form})


def edit(request):
    if request.method == "POST":

        user_form = UserEditForm(instance=request.user, data=request.POST)
        # profile_form = ProfileEditForm(
        #                             instance=request.user.profile,
        #                             data=request.POST,
        #                             files=request.FILES)
        if user_form.is_valid():  # and profile_form.is_valid():
            user_form.save()
        # profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    # profile_form = ProfileEditForm(
    #  instance=request.user.profile)
    return render(request, "service/res/edit.html", {"user_form": user_form})
    #'profile_form': profile_form})


def event(request):
    now = timezone.now()
    upcoming_events = Event.objects.filter(date__gte=now.date())

    past_events = Event.objects.filter(date__lt=now.date()).order_by("-date")[:5]

    return render(
        request,
        "service/res/events.html",
        {"upcoming_events": upcoming_events, "past_events": past_events},
    )


def event_info(request, name):
    ev_info = Event.objects.all()
    e_info = get_object_or_404(ev_info, name=name)
    e_date = e_info.date
    ev_date = datetime.strptime(e_date.strftime("%Y-%m-%d"), "%Y-%m-%d")

    user = request.user
    when = None

    if request.method == "POST":
        when = ReminderForm(request.POST)
        reminder_time_str = request.POST.get("reminder_time")

        reminder_time = datetime.strptime(reminder_time_str, "%Y-%m-%dT%H:%M")

        # Ensure reminder is in the future
        if datetime.now() >= reminder_time:
            messages.error(request, "Reminder time must be in the future.")
            return redirect("service:event_info", name)

        if reminder_time >= ev_date:
            messages.error(request, "the date is past the event date.")
            return redirect("service:event_info", name)

        Reminder.objects.create(user=user, event=e_info, reminder_time=reminder_time)

        messages.success(request, "Reminder set successfully!")

        tar = request.user.first_name
        targett = str(tar)
        e_url = request.build_absolute_uri(e_info.get_absolute_url())
        the_reminder_time_str = request.POST.get("reminder_time")
        the_reminder_time = datetime.strptime(the_reminder_time_str, "%Y-%m-%dT%H:%M")
        a_reminder_time = timezone.make_aware(the_reminder_time)

        subject = "Reminder: Upcoming Event"
        message = f"JAMBO! {targett}. ST.RAYAN is writing to remind you of the {e_info.name} event that is coming up soon. click the following link to view more {e_url}"

        from_email = settings.EMAIL_HOST_USER
        to_email = [request.user.email]
        # Schedule the Celery task to run at the reminder time
        send_reminder_email.apply_async(
            (
                subject,
                message,
                from_email,
                to_email,
            ),
            eta=a_reminder_time,  # eta parameter schedules the task at the specified time
        )

        return redirect("service:event_info", name)
    else:
        when = ReminderForm()

    context = {"e_info": e_info, "when": when}  # Assuming ReminderForm
    return render(request, "service/res/event_info.html", context)

    # from datetime import timedelta


def delete_reminder(request, id):
    store = Reminder.objects.all()
    item = None
    current_user = request.user
    user_reminders = Reminder.objects.filter(user=current_user)

    if request.method == "POST":

        item = get_object_or_404(store, pk=id)
        item.delete()
        messages.success(request, "Reminder deleted successfully!")
        return redirect("service:account")
    else:
        pass
    return render(request, "service/res/account.html", {"rmb": user_reminders})


def meeting(request):
    meeting = Room.objects.filter(room_type__name="meeting")

    room_type = get_object_or_404(
        RoomType.objects.prefetch_related("amenities"), name="meeting"
    )
    today = timezone.now().date()
    hotel = get_object_or_404(Hotel)

    form = RoomAvailabilityForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        start_date = form.cleaned_data["start_date"]
        duration = form.cleaned_data["duration"]
        end_date = start_date + timedelta(days=duration - 1)

        # Filter available rooms based on the selected date range
        available_rooms = Room.objects.filter(
            Q(room_type__name="meeting")
            & (
                ~Q(
                    availabilities__start_date__lte=end_date,
                    availabilities__end_date__gte=start_date,
                )
                | ~Q(availabilities__isnull=False)
            )
        ).distinct()

        all_rooms = Room.objects.filter(room_type__name="meeting").annotate(
            is_available=Exists(available_rooms.filter(pk=OuterRef("pk")))
        )

        return render(
            request,
            "service/res/rooms.html",
            {
                "hotel": hotel,
                "amn": room_type,
                "name": "roomtype",
                "room": all_rooms,
                "start_date": start_date,
                "duration": duration,
                "form": form,
            },
        )

    start_date = form.initial.get("start_date", today)
    duration = form.initial.get("duration", 1)
    end_date = start_date + timedelta(days=duration - 1)
    room = Room.objects.filter(room_type__name="meeting")

    available_rooms = Room.objects.filter(
        Q(room_type__name="meeting")
        & (
            ~Q(
                availabilities__start_date__lte=end_date,
                availabilities__end_date__gte=start_date,
            )
            | ~Q(availabilities__isnull=False)
        )
    ).distinct()
    all_rooms = Room.objects.filter(room_type__name="meeting").annotate(
        is_available=Exists(available_rooms.filter(pk=OuterRef("pk")))
    )

    return render(
        request,
        "service/res/rooms.html",
        {
            "hotel": hotel,
            "amn": room_type,
            "name": "roomtype",
            "room": all_rooms,
            "today": today,
            "start_date": start_date,
            "duration": duration,
            "form": form,
        },
    )


def booking(request):
    cart_room_form = CartAddRoomForm()
    if request.method == "POST":

        typ = None
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            room_type_id = form.cleaned_data["room_type"]

            if room_type_id:
                all_rooms = (
                    Room.objects.filter(room_type_id=room_type_id)
                    .select_related("room_type")
                    .prefetch_related("room_type__amenities")
                )
                rtp = get_object_or_404(RoomType, pk=room_type_id)
                typ = rtp.name
            else:
                all_rooms = Room.objects.select_related("room_type").prefetch_related(
                    "room_type__amenities"
                )
                typ = "all"
            # Filter out rooms with bookings overlapping the specified date range
            booked_rooms = Room.objects.filter(
                availabilities__start_date__lte=end_date,
                availabilities__end_date__gte=start_date,
            )

            available_rooms_with_details = []

            for room in all_rooms:
                if room not in booked_rooms:
                    if room.is_available_for_dates(
                        start_date=start_date, end_date=end_date
                    ):
                        room_details = {
                            "room": room,
                            "room_type": room.room_type,
                            "amenities": room.room_type.amenities.all(),
                            "images": room.image,
                            "price": room.room_type.price,
                        }
                        available_rooms_with_details.append(room_details)

            context = {
                "typ": typ,
                "form": form,
                "today": available_rooms_with_details,
                "sd": start_date,
                "ed": end_date,
                "cart": cart_room_form,
            }
            return render(request, "service/res/booking.html", context)

        else:
            # If form is not valid, render it again with validation errors
            error_message = "The start date is either past or the end date is before the start date of reservation, please correct that."
            messages.error(request, error_message)
            return render(request, "service/res/booking.html", {"form": form})
    else:
        form = DateRangeForm()
        today = timezone.now().date()
        tommorow = today + timedelta(days=1)
        typ = "all"
        all_rooms = (
            Room.objects.select_related("room_type")
            .prefetch_related("room_type__amenities")
            .all()
        )

        available_rooms_with_details = []

        for room in all_rooms:
            if room.is_available_for_dates(start_date=today, end_date=today):
                room_details = {
                    "room": room,
                    "room_type": room.room_type,
                    "amenities": room.room_type.amenities.all(),
                    "images": room.image,
                    "price": room.room_type.price,
                }
                available_rooms_with_details.append(room_details)

        context = {
            "today": available_rooms_with_details,
            "form": form,
            "sd": today,
            "ed": tommorow,
            "typ": typ,
            "cart": cart_room_form,
        }
        return render(request, "service/res/booking.html", context)


def payment_confirmation(request):
    if request.method == "POST":
        # Process the callback data as per M-Pesa API documentation
        # Update transaction status in database
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
    return JsonResponse({"ResultCode": 1, "ResultDesc": "Rejected"})


def admin_page(request):

    return render(request, "service/res/admin.html")


def email_view(request):
    if request.method == "POST":
        email_subject = request.POST.get("email_subject")
        email_content = request.POST.get("email_content")
        specific_user_email = request.POST.get("specific_user_email")
        send_to_all = request.POST.get("send_to_all") == "true"

        if send_to_all:
            users = User.objects.all()
            recipient_list = [user.email for user in users]
        elif specific_user_email:
            recipient_list = [specific_user_email]
        else:
            recipient_list = []

        if recipient_list:
            send_mail(
                email_subject,
                email_content,
                settings.EMAIL_HOST_USER,
                recipient_list,
                fail_silently=False,
            )
            return redirect(
                "service:success_page"
            )  # Redirect to success page after sending

    return render(request, "service/res/admin.html")


def success_page(request):
    return render(request, "service/res/success.html")


def handle_message(request=None):
    if request.method == "POST":
        # Create a ContactForm instance with the POST data
        inquiry = ContactForm(data=request.POST)

        if inquiry.is_valid():
            # Extract form data
            name = inquiry.cleaned_data["name"]
            from_email = inquiry.cleaned_data["email"]
            subject = inquiry.cleaned_data["subject"]
            message = (
                f"{inquiry.cleaned_data['message']}\n"
                f"[This message was sent by {name} - {from_email}]"
            )

            # Send the email
            send_mail(
                subject,
                message,
                from_email,  # From email
                [settings.EMAIL_HOST_USER],  # To email
                fail_silently=False,
            )

            messages.success(request, "Email has been sent successfully.")
            return render(request, "service/res/index.html")

        else:
            messages.error(request, "There was an error with your submission.")
    else:
        inquiry = ContactForm()

    return inquiry


def text(request):
    form = handle_message(request)

    context = {
        "form": form,
    }

    return render(request, "service/res/index.html", context)
