import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.timezone import now
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.forms import SetPasswordForm



from .models import (
    Profile,
    Holiday,
    TournamentBooking,
    TournamentSlot,
)

# =====================================================
# AUTH
# =====================================================
@csrf_protect
def auth_view(request):
    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "register":
            email = request.POST.get("email")
            password = request.POST.get("password")
            name = request.POST.get("name")
            age = request.POST.get("age")
            gender = request.POST.get("gender")
            image = request.FILES.get("profile_image")

            if User.objects.filter(username=email).exists():
                messages.error(request, "Email already registered")
                return redirect("auth")

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name,
            )

            profile = user.profile
            profile.age = age
            profile.gender = gender
            if image:
                profile.profile_image = image
            profile.save()

            messages.success(request, "Registration successful")
            return redirect("auth")

        if form_type == "login":
            user = authenticate(
                request,
                username=request.POST.get("email"),
                password=request.POST.get("password"),
            )
            if user:
                login(request, user)
                return redirect("dashboard")

            messages.error(request, "Invalid credentials")
            return redirect("auth")

    return render(request, "auth/auth.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("auth")


# =====================================================
# DASHBOARD
# =====================================================

# =========================
# DASHBOARD
# =========================
@login_required
def dashboard_view(request):
    user = request.user

    slots = TournamentSlot.objects.filter(
        booking__user=user
    )

    holidays = Holiday.objects.all()

    calendar_slots = [
        {
            "date": s.date.strftime("%Y-%m-%d"),
            "status": s.status
        }
        for s in slots
    ]

    calendar_holidays = [
        {
            "date": h.date.strftime("%Y-%m-%d"),
            "name": h.name
        }
        for h in holidays
    ]

    context = {
        "active_page": "dashboard",

        "total_bookings": slots.count(),
        "active_bookings": slots.filter(status="BOOKED").count(),
        "holiday_bookings": slots.filter(status="SHIFTED").count(),
        "cancelled_bookings": slots.filter(status="CANCELLED").count(),

        "calendar_slots": json.dumps(calendar_slots),
        "calendar_holidays": json.dumps(calendar_holidays),
    }

    return render(request, "dashboard/dashboard.html", context)


# =====================================================
# CALENDAR
# =====================================================
@login_required
def booking_calendar_view(request):
    return render(request, "bookings/calendar.html", {
        "active_page": "bookings"
    })


# =====================================================
# PAYMENT (FAKE)
# =====================================================
@login_required
def payment_page(request):
    return render(request, "bookings/payment.html", {
        "active_page": "bookings"
    })


@login_required
@csrf_exempt
def payment_success(request):
    if request.method != "POST":
        return JsonResponse({"success": False})

    data = json.loads(request.body)
    plan = data.get("plan")
    slots = data.get("slots", [])

    if not plan or not slots:
        return JsonResponse({"success": False, "error": "Invalid payload"})

    user = request.user
    total_slots = len(slots)
    total_amount = 2400 if plan == "MONTHLY" else total_slots * 300

    booking = TournamentBooking.objects.create(
        user=user,
        plan_type=plan,
        start_date=min(s["date"] for s in slots),
        end_date=max(s["date"] for s in slots),
        total_slots=total_slots,
        total_amount=total_amount,
    )

    for s in slots:
        TournamentSlot.objects.create(
            booking=booking,
            date=s["date"],
            start_time=s["start"],
            end_time=s["end"],
            price=300,
            status="BOOKED",
        )

    send_booking_email(user, booking)

    return JsonResponse({"success": True})


@login_required
def payment_success_page(request):
    return render(request, "bookings/payment_success.html", {
        "active_page": "view_bookings"
    })


# =====================================================
# VIEW BOOKINGS
# =====================================================
@login_required
def view_bookings(request):
    bookings = (
        TournamentBooking.objects
        .filter(user=request.user)
        .prefetch_related("slots")
    )

    return render(request, "bookings/view_bookings.html", {
        "bookings": bookings,
        "active_page": "view_bookings"
    })


# =====================================================
# HOLIDAY CHECK (AJAX)
# =====================================================
@login_required
@csrf_exempt
def check_holiday(request):
    data = json.loads(request.body)
    date = data.get("date")

    holiday = Holiday.objects.filter(date=date).first()

    if holiday and holiday.is_blocking():
        return JsonResponse({
            "is_holiday": True,
            "name": holiday.name
        })

    return JsonResponse({"is_holiday": False})


# =====================================================
# RESCHEDULE SLOT
# =====================================================
@login_required
@csrf_exempt
def reschedule_slot(request, slot_id):
    if request.method != "POST":
        return JsonResponse({"success": False})

    data = json.loads(request.body)
    new_date = data.get("date")

    slot = TournamentSlot.objects.filter(
        id=slot_id,
        booking__user=request.user
    ).first()

    if not slot:
        return JsonResponse({"success": False, "error": "Slot not found"})

    holiday = Holiday.objects.filter(date=new_date).first()

    slot.date = new_date

    if holiday and holiday.is_blocking():
        slot.status = "SHIFTED"
        slot.save()
        send_reschedule_email(request.user, slot, holiday.name)

        return JsonResponse({
            "success": True,
            "shifted": True,
            "holiday": holiday.name
        })

    slot.status = "BOOKED"
    slot.save()
    send_reschedule_email(request.user, slot)

    return JsonResponse({"success": True})


# =====================================================
# DELETE SLOT
# =====================================================
@login_required
@csrf_exempt
def delete_slot(request, slot_id):
    if request.method != "POST":
        return JsonResponse({"success": False})

    slot = TournamentSlot.objects.filter(
        id=slot_id,
        booking__user=request.user
    ).first()

    if not slot:
        return JsonResponse({"success": False})

    slot.status = "CANCELLED"
    slot.save()
    send_cancel_email(request.user, slot)

    return JsonResponse({"success": True})


# =====================================================
# EMAIL HELPERS
# =====================================================
def build_slot_table(slots):
    rows = ""
    for s in slots:
        rows += f"""
        <tr>
          <td style="border:1px solid #ddd;padding:8px;">{s.date}</td>
          <td style="border:1px solid #ddd;padding:8px;">
            {s.start_time} – {s.end_time}
          </td>
          <td style="border:1px solid #ddd;padding:8px;">₹{s.price}</td>
          <td style="border:1px solid #ddd;padding:8px;">{s.status}</td>
        </tr>
        """
    return f"""
    <table style="border-collapse:collapse;width:100%;">
      <thead>
        <tr style="background:#f3f4f6;">
          <th>Date</th><th>Time</th><th>Price</th><th>Status</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
    """


def send_booking_email(user, booking):
    table = build_slot_table(booking.slots.all())

    html = f"""
    <h2>Hi {user.first_name},</h2>
    <p>Your tournament booking is confirmed.</p>
    <p><strong>Plan:</strong> {booking.get_plan_type_display()}</p>
    <p><strong>Total Paid:</strong> ₹{booking.total_amount}</p>
    {table}
    <p>Regards,<br><strong>ChessHub Team</strong></p>
    """

    email = EmailMultiAlternatives(
        "Tournament Booking Confirmed | ChessHub",
        "Booking confirmed",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
    email.attach_alternative(html, "text/html")
    email.send()


def send_reschedule_email(user, slot, holiday_name=None):
    table = build_slot_table([slot])

    note = (
        f"<p><strong>Reason:</strong> Holiday – {holiday_name}</p>"
        if holiday_name else ""
    )

    html = f"""
    <h2>Slot Updated</h2>
    <p>Your tournament slot has been rescheduled.</p>
    {note}
    {table}
    <p>Regards,<br><strong>ChessHub Team</strong></p>
    """

    email = EmailMultiAlternatives(
        "Slot Rescheduled | ChessHub",
        "Slot updated",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
    email.attach_alternative(html, "text/html")
    email.send()


def send_cancel_email(user, slot):
    table = build_slot_table([slot])

    html = f"""
    <h2>Slot Cancelled</h2>
    <p>Your tournament slot has been cancelled.</p>
    {table}
    <p>Regards,<br><strong>ChessHub Team</strong></p>
    """

    email = EmailMultiAlternatives(
        "Slot Cancelled | ChessHub",
        "Slot cancelled",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
    email.attach_alternative(html, "text/html")
    email.send()





class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = SetPasswordForm
    template_name = "auth/password_reset_confirm.html"
    success_url = "/password-reset/complete/"

    def post(self, request, *args, **kwargs):
        self.object = self.get_user(kwargs["uidb64"])

        password1 = request.POST.get("new_password1")
        password2 = request.POST.get("new_password2")

        if password1 and password1 == password2:
            self.object.set_password(password1)
            self.object.save(update_fields=["password"])

            return redirect(self.success_url)

        messages.error(request, "Passwords do not match")
        return render(request, self.template_name)
