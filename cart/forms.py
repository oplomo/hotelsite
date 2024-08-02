from django import forms

ROOM_DURATION_CHOICES = [(i, str(i)) for i in range(1, 31)]
NUMBER_OF_GUEST_CHOICES = [(i, str(i)) for i in range(1, 7)]


class CartAddRoomForm(forms.Form):
    duration = forms.TypedChoiceField(
        choices=ROOM_DURATION_CHOICES, coerce=int, initial=1
    )
    number_of_guest = forms.TypedChoiceField(
        choices=NUMBER_OF_GUEST_CHOICES, coerce=int, initial=1
    )
    override_duration = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput
    )
    override_number_of_guest = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput
    )
