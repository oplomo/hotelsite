from decimal import Decimal
from django.conf import settings
from service.models import Room
from datetime import timedelta
from django.utils import timezone


class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(
        self,
        room_instance,
        duration=1,
        override_duration=False,
        number_of_guest=1,
        override_number_of_guest=False,
        start_date=timezone.now().date(),
        end_date=timezone.now().date() + timezone.timedelta(days=1),
    ):

        # Add a product to the cart or update its quantity.
        room_number = str(room_instance.number)
        if room_number not in self.cart:
            self.cart[room_number] = {
                "duration": 0,
                "number_of_guest": 0,
                "start_date": start_date,
                "end_date": end_date,
                "price": str(room_instance.room_type.price),
            }
        if override_duration:

            self.cart[room_number]["duration"] = duration
        else:

            self.cart[room_number]["duration"] += duration
        if override_number_of_guest:
            self.cart[room_number]["number_of_guest"] = number_of_guest
        else:
            self.cart[room_number]["number_of_guest"] += number_of_guest

        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved

        self.session.modified = True

    def remove(self, room_num):
        # Remove a product from the cart.

        room_number = str(room_num)
        if room_number in self.cart:
            del self.cart[room_number]
            self.save()

    def __iter__(self):
        # Iterate over the items in the cart and get the products from the database.

        room_numbers = self.cart.keys()
        # get the product objects and add them to the cart
        rooms = Room.objects.filter(number__in=room_numbers)
        cart = self.cart.copy()
        for room in rooms:
            cart[str(room.number)]["room"] = room
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = (
                (item["price"] / 2) + (item["number_of_guest"] * (item["price"]) / 2)
            ) * item["duration"]
            yield item

    def __len__(self):
        # Count all items in the cart.
        count = 0
        for item in self.cart.values():
            count += 1

        return count

    def get_total_price(self):

        return sum(
            (
                (Decimal(item["price"]) / 2)
                + (item["number_of_guest"] * (Decimal(item["price"]) / 2))
            )
            * item["duration"]
            for item in self.cart.values()
        )

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
