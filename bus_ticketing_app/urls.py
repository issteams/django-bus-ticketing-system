from . import views
from django.urls import path

app_name = 'bus_ticketing_app'
urlpatterns = [
    path('', views.indexView, name='index'),
    path('admin/login/', views.adminView, name='adminlogin'),
    path("driver/login/", views.driverLoginView, name='driverlogin'),
    path("passenger/login/", views.passengerLoginView, name='userLogin'),
    path("driver/signup/", views.driverSignUpView, name='driversignup'),

    path("Routes/", views.bus_route, name="bus_route"),
    path("search_route/", views.search_bus_route, name="bus_route_result"),

    path("user/signup/", views.userSignUp, name='userSignUp'),
    path("user/signin/", views.userSignIn, name='userSignIn'),

    path("driver/signup/", views.driverSignUp, name='driverSignUp'),
    path("driver/signin/", views.driverLogin, name='driverSignIn'),

    path("book/", views.book, name='book'),
    path("home/", views.user_home, name="user_home"),

    path("logout/", views.userLogOut, name="logout"),
]