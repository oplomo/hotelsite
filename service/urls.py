from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


app_name = "service"

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("restaurant/", views.Restaurant_page.as_view(), name="restaurant"),
    path("restaurant/<str:name>/", views.dish_r, name="dish_r"),
    path("wellness/<str:name>/", views.dish_w, name="dish_w"),
    path("about/", views.about, name="about"),
    path("account/", views.account, name="account"),
    path("gallery/", views.gallery, name="gallery"),
    path("wellness/", views.wellness, name="wellness"),
    path("register/", views.register, name="register"),
    path("edit/", views.edit, name="edit"),
    path("events/", views.event, name="event"),
    path("event_info/<str:name>/", views.event_info, name="event_info"),
    path("event_info/delete/<int:id>/", views.delete_reminder, name="delete_r"),
    path("roomt/<int:id>/", views.rooms, name="rooms"),
    path("roomtypes/", views.Roomtype, name="roomtype"),
    path("meeting/", views.meeting, name="meeting"),
    path("booking/", views.booking, name="booking"),
    path("admin_page/", views.admin_page, name="admin"),
    path("email/", views.email_view, name="email_view"),
    path("success/", views.success_page, name="success_page"),
    path('contact/', views.text, name='contact_view'),
    path('success/', views.success_page, name='success_page'),
]
