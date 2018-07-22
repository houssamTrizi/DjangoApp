from django.conf.urls import url
from basic_app import views

app_name = "basic_app"

urlpatterns = [
    url(r"^registration/$", views.registration, name="registration"),
    url(r"^login/$", views.user_login, name="user_login"),
    url(r"^logout/$", views.user_logout, name="user_logout")
]
