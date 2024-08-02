from .models import Hotel


def hotel_details(request):
    details = Hotel.objects.all()
    lenth = len(details)
    return {"details": details, "len": lenth}
