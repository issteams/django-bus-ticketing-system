from . import views, AdminViews, StaffViews, UserViews
from django.urls import path

app_name = 'bus_ticketing_app'
urlpatterns = [
    # Admin Views
    path('', views.indexView, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path("user_signup/", views.userSignUp, name='userSignUp'),
    path('doLogin/', views.doLogin, name='do_login'),
    path('admin_home/', AdminViews.admin_home, name='admin_home'),
    path('staff/', AdminViews.staff, name='staff'),
    path('staff/add_staff/', AdminViews.add_staff, name='add_staff'),
    path('staff/add_staff_save/', AdminViews.add_staff_save, name='add_staff_save'),
    path('staff/edit_staff/<str:staff_id>/', AdminViews.edit_staff, name='edit_staff'),
    path('staff/edit_staff_save/', AdminViews.edit_staff_save, name='edit_staff_save'),
    path('staff/delete_staff/<str:staff_id>/', AdminViews.delete_staff, name='delete_staff'),
    path('passenger/', AdminViews.passenger, name='passenger'),
    path('passenger/add_passenger/', AdminViews.add_passenger, name='add_passenger'),
    path('passenger/add_passenger_save/', AdminViews.add_passenger_save, name='add_passenger_save'),
    path('passenger/edit_passenger/<str:passenger_id>/', AdminViews.edit_passenger, name='edit_passenger'),
    path('passenger/edit_passenger_save/', AdminViews.edit_passenger_save, name='edit_passenger_save'),
    path('passenger/delete_passenger/<str:passenger_id>/', AdminViews.delete_passenger, name='delete_passenger'),
    path('bus_route/', AdminViews.bus_route, name='bus_route'),
    path('bus_route/add_bus_route/', AdminViews.add_bus_route, name='add_bus_route'),
    path('bus_route/add_bus_route_save/', AdminViews.add_bus_route_save, name='add_bus_route_save'),
    path('bus_route/edit_bus_route/<str:bus_route_id>/', AdminViews.edit_bus_route, name='edit_bus_route'),
    path('bus_route/edit_bus_route_save/', AdminViews.edit_bus_route_save, name='edit_bus_route_save'),
    path('bus_route/delete_bus_route/<str:bus_route_id>/', AdminViews.delete_bus_route, name='delete_bus_route'),
    path('bus/', AdminViews.bus, name='bus'),
    path('bus/add_bus/', AdminViews.add_bus, name='add_bus'),
    path('bus/add_bus_save/', AdminViews.add_bus_save, name='add_bus_save'),
    path('bus/edit_bus/<str:bus_id>/', AdminViews.edit_bus, name='edit_bus'),
    path('bus/edit_bus_save/', AdminViews.edit_bus_save, name='edit_bus_save'),
    path('bus/delete_bus/<str:bus_id>', AdminViews.delete_bus, name='delete_bus'),
    path('schedule/', AdminViews.schedule, name='schedule'),
    path('schedule/add_schedule/', AdminViews.add_schedule, name='add_schedule'),
    path('schedule/add_schedule_save/', AdminViews.add_schedule_save, name='add_schedule_save'),
    path('schedule/edit_schedule/<str:schedule_id>/', AdminViews.edit_schedule, name='edit_schedule'),
    path('schedule/edit_schedule_save/', AdminViews.edit_schedule_save, name='edit_schedule_save'),
    path('schedule/delete_schedule/<str:schedule_id>', AdminViews.delete_schedule, name='delete_schedule'),
    path('payment/', AdminViews.payment, name='payment'),
    path('payment/add_payment/', AdminViews.add_payment, name='add_payment'),
    path('payment/add_payment_save/', AdminViews.add_payment_save, name='add_payment_save'),
    path('payment/edit_payment/<str:payment_id>/', AdminViews.edit_payment, name='edit_payment'),
    path('payment/edit_payment_save/', AdminViews.edit_payment_save, name='edit_payment_save'),
    path('payment/payment/delete_payment/<str:payment_id>/', AdminViews.delete_payment, name='delete_payment'),
    path('ticket/', AdminViews.ticket, name='ticket'),
    path('ticket/add_ticket/', AdminViews.add_ticket, name='add_ticket'),
    path('ticket/add_ticket_save/', AdminViews.add_ticket_save, name='add_ticket_save'),
    path('ticket/edit_ticket/<str:ticket_id>/', AdminViews.edit_ticket, name='edit_ticket'),
    path('ticket/edit_ticket_save/', AdminViews.edit_ticket_save, name='edit_ticket_save'),
    path('ticket/delete_ticket/<str:ticket_id>/', AdminViews.delete_ticket, name='delete_ticket'),
    path('admin_profile/', AdminViews.admin_profile, name='admin_profile'),
    path('admin_profile_save/', AdminViews.admin_profile_save, name='admin_profile_save'),



   # Staff Urls
   path('staff_home/', StaffViews.staff_home, name='staff_home'),

   # User Urls
   path('user_home/', UserViews.user_home, name='user_home'),
   path("search_result/", UserViews.search_result, name='search_result'),
   path("book_seat/<str:schedule_id>/", UserViews.book_seat, name='book_seat'),
   path("get_book_seat/<str:schedule_id>/", UserViews.get_book_seat, name='get_book_seat'),
   path("make_payment/<str:schedule_id>/", UserViews.make_payment, name='make_payment'),
   path("verify_payment/", UserViews.verify_payment, name='verify_payment'),
   path("payment_success/", UserViews.payment_success, name='payment_success'),
   path("user_tickets/", UserViews.user_tickets, name='user_tickets'),
   path("user_payments/", UserViews.user_payments, name='user_payments'),
   path("print_ticket/<str:ticket_id>/", UserViews.print_ticket, name='print_ticket'),

   # Log Out Url
   path("logout/", views.userLogOut, name="logout"),
]