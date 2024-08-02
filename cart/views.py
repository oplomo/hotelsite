from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from service.models import Room
from .cart import Cart
from .forms import CartAddRoomForm



# payments/views.py




@require_POST
def cart_add(request, room_number):
    cart = Cart(request)
    room = get_object_or_404(Room, number=room_number)
    form = CartAddRoomForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            room_instance=room,
            duration=cd["duration"],
            number_of_guest=cd["number_of_guest"],
            override_duration=cd["override_duration"],
            override_number_of_guest=cd["override_number_of_guest"],
            start_date=request.POST.get("start_date"),
            end_date=request.POST.get("end_date"),
        )

    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, room_number):
    cart = Cart(request)
    room_num = get_object_or_404(Room, number=room_number)
    cart.remove(room_num.number)
    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item["update_room_form"] = CartAddRoomForm(
            initial={
                "duration": item["duration"],
                "number_of_guest": item["number_of_guest"],
                "override_duration": True,
                "override_number_of_guest": True,
                "start_date": item.get("start_date"),
                "end_date": item.get("end_date"),
            }
        )

    return render(request, "cart/detail.html", {"cart": cart})



