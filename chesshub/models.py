from django.db import models
from django.contrib.auth.models import User


# =========================
# USER PROFILE
# =========================
class Profile(models.Model):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    profile_image = models.ImageField(
        upload_to='profiles/',
        default='profiles/default.png'
    )

    login_attempts = models.PositiveIntegerField(default=0)
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


# =========================
# HOLIDAYS
# =========================
class Holiday(models.Model):

    HOLIDAY_TYPE_CHOICES = (
        ('GAZETTED', 'Gazetted Holiday'),
        ('RESTRICTED', 'Restricted Holiday'),
        ('OBSERVANCE', 'Observance'),
        ('SEASON', 'Season'),
    )

    date = models.DateField(unique=True)
    name = models.CharField(max_length=200)
    holiday_type = models.CharField(
        max_length=20,
        choices=HOLIDAY_TYPE_CHOICES
    )

    def is_blocking(self):
        """
        Only these holidays block tournaments
        """
        return self.holiday_type in ['GAZETTED', 'RESTRICTED']

    def __str__(self):
        return f"{self.date} - {self.name}"


# =========================
# TOURNAMENT BOOKING (PARENT)
# =========================
class TournamentBooking(models.Model):

    PLAN_CHOICES = (
        ('BASIC', 'Basic'),
        ('MONTHLY', 'Monthly'),
        ('CUSTOM', 'Custom'),
    )

    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tournament_bookings'
    )

    plan_type = models.CharField(
        max_length=10,
        choices=PLAN_CHOICES
    )

    start_date = models.DateField()
    end_date = models.DateField()

    total_slots = models.PositiveIntegerField()
    total_amount = models.PositiveIntegerField()  # total_slots × 300

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} | {self.plan_type} | ₹{self.total_amount}"


# =========================
# INDIVIDUAL TOURNAMENT SLOTS
# =========================
class TournamentSlot(models.Model):

    SLOT_STATUS_CHOICES = (
        ('BOOKED', 'Booked'),
        ('SHIFTED', 'Shifted due to Holiday'),
        ('CANCELLED', 'Cancelled'),
    )

    booking = models.ForeignKey(
        TournamentBooking,
        on_delete=models.CASCADE,
        related_name='slots'
    )

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    price = models.PositiveIntegerField(default=300)

    status = models.CharField(
        max_length=15,
        choices=SLOT_STATUS_CHOICES,
        default='BOOKED'
    )

    def __str__(self):
        return f"{self.date} | {self.start_time}-{self.end_time}"



class Booking(models.Model):

    PLAN_CHOICES = (
        ("BASIC", "Basic"),
        ("MONTHLY", "Monthly"),
        ("CUSTOM", "Custom"),
    )

    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("HOLIDAY", "Holiday"),
        ("RESCHEDULED", "Rescheduled"),
        ("CANCELLED", "Cancelled"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES)

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    is_holiday = models.BooleanField(default=False)
    holiday_name = models.CharField(max_length=100, blank=True, null=True)

    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default="ACTIVE"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "start_time"]

    def __str__(self):
        return f"{self.user.email} | {self.date}"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.OneToOneField(
        TournamentBooking,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    razorpay_order_id = models.CharField(max_length=255)
    razorpay_payment_id = models.CharField(max_length=255, blank=True)
    amount = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("CREATED", "CREATED"),
            ("SUCCESS", "SUCCESS"),
            ("FAILED", "FAILED"),
        ],
        default="CREATED"
    )
    created_at = models.DateTimeField(auto_now_add=True)
