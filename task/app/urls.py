from django.urls import path
from . import views
urlpatterns = [
    path("home",views.homepage,name="home"),
    path("register",views.register,name="register"),
    path("",views.register,name="default"),
    path("login",views.login,name="login"),
    path("result",views.showRes,name="showRes"),
    path("logout",views.logout,name="logout")
]


