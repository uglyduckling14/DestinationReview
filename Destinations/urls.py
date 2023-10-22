from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("users/new", views.sign_up, name = "sign_up"),
    path("sessions", views.sign_in, name = "sign_exist"),
    path("destinations", views.destinations_page, name = "destinations"),
    path("new_destinations", views.new_destination, name = "create_destination"),
    path("sessions/new", views.sign_in, name ="sign_in" ),
    path("users", views.sign_up, name = "sign_new"),
    path("destinations/<int:id>", views.update_destination, name="edit"),
    path("destinations/<int:id>/destroy", views.destroy_destination, name="destroy_dest"),
    path("sessions/destroy", views.destroy_session, name = "destroy_session")
]