from django.urls import path
from Home import views

urlpatterns = [
    path("", views.home, name='home'),
    path("signup", views.signup, name='signup'),
    path("login", views.signing, name='login'),
    path("logout", views.signout, name='logout'),
    path("logged", views.logged, name='logged'),
]