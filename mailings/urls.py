from django.urls import path

from .views import (add_message, delete_message, edit_message, home, messages,
                    recipients)

urlpatterns = [
    path("", home, name="home"),
    path("messages/", messages, name="messages"),
    path("add-message/", add_message, name="add_message"),
    path("edit-message/<int:id>/", edit_message, name="edit_message"),
    path("delete-message/<int:id>/", delete_message, name="delete_message"),
    path("recipients/", recipients, name="recipients"),
]
