from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("roles/", views.role_list, name="role_list"),
    path("roles/create/", views.role_create, name="role_create"),
    path("roles/<int:group_id>/edit/", views.role_edit, name="role_edit"),
    path("roles/<int:group_id>/delete/", views.role_delete, name="role_delete"),
]