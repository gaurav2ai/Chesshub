from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from chesshub.views_calendar import calendar_api

urlpatterns = [
    path('', auth_view, name='auth'),

    # ---------- PASSWORD RESET ----------
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='auth/password_reset.html',
            email_template_name='auth/password_reset_email.html',
            success_url='/password-reset/done/'
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='auth/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
path(
    "reset/<uidb64>/<token>/",
    CustomPasswordResetConfirmView.as_view(),
    name="password_reset_confirm",
),



    path(
        'password-reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='auth/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    # ---------- CORE ----------
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),

    # ---------- CALENDAR ----------
    path('api/calendar/', calendar_api, name='calendar_api'),
    path('bookings/calendar/', booking_calendar_view, name='booking_calendar'),

    # ---------- BOOKINGS ----------
    path('bookings/', view_bookings, name='view_bookings'),

    # ---------- PAYMENT FLOW ----------
    path('bookings/payment/', payment_page, name='payment'),
    path('bookings/payment/success/', payment_success, name='payment_success'),
    path(
  "bookings/payment/success-page/",
  payment_success_page,
  name="payment_success_page"
),

path(
        "bookings/slot/delete/<int:slot_id>/",
        delete_slot,
        name="delete_slot"
    ),

    path(
        "bookings/slot/reschedule/<int:slot_id>/",
        reschedule_slot,
        name="reschedule_slot"
    ),

path("bookings/check-holiday/", check_holiday, name="check_holiday"),



]
