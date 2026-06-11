from datetime import date, datetime, timedelta, time
from django.utils.timezone import now
from chesshub.models import Holiday, TournamentBooking, TournamentSlot

SLOT_PRICE = 300


# ----------------------------------
# UTILS
# ----------------------------------
def is_blocking_holiday(check_date):
    """
    Returns True if date is Gazetted or Restricted holiday
    """
    return Holiday.objects.filter(
        date=check_date,
        holiday_type__in=['GAZETTED', 'RESTRICTED']
    ).exists()


def get_next_valid_date(original_date, weekday):
    """
    Carry forward to next same weekday which is not a blocking holiday
    """
    next_date = original_date

    while True:
        if next_date.weekday() == weekday and not is_blocking_holiday(next_date):
            return next_date
        next_date += timedelta(days=1)


def generate_hour_slots(start_hour, end_hour):
    """
    Generates fixed 1-hour slots
    """
    slots = []
    for hour in range(start_hour, end_hour):
        slots.append(
            (time(hour, 0), time(hour + 1, 0))
        )
    return slots


# ----------------------------------
# BASIC PLAN (1 day / week × 4 weeks)
# ----------------------------------
def generate_basic_plan_slots(booking, weekday, start_hour, end_hour):
    """
    weekday: 0=Mon ... 6=Sun
    """
    today = date.today()
    slots_created = []

    hour_slots = generate_hour_slots(start_hour, end_hour)

    weeks_generated = 0
    current_date = today

    while weeks_generated < 4:
        if current_date.weekday() == weekday:
            final_date = (
                current_date if not is_blocking_holiday(current_date)
                else get_next_valid_date(current_date, weekday)
            )

            for start, end in hour_slots:
                slots_created.append(
                    TournamentSlot(
                        booking=booking,
                        date=final_date,
                        start_time=start,
                        end_time=end,
                        price=SLOT_PRICE,
                        status='SHIFTED' if final_date != current_date else 'BOOKED'
                    )
                )

            weeks_generated += 1
            current_date += timedelta(days=7)
        else:
            current_date += timedelta(days=1)

    return slots_created


# ----------------------------------
# MONTHLY PLAN (2 days / week × 4 weeks)
# ----------------------------------
def generate_monthly_plan_slots(booking, weekdays, start_hour, end_hour):
    """
    weekdays: list of two weekdays [0, 4] for Mon & Fri
    """
    today = date.today()
    end_date = today + timedelta(days=30)

    hour_slots = generate_hour_slots(start_hour, end_hour)
    slots_created = []

    current_date = today

    while current_date <= end_date:
        if current_date.weekday() in weekdays:
            final_date = (
                current_date if not is_blocking_holiday(current_date)
                else get_next_valid_date(current_date, current_date.weekday())
            )

            for start, end in hour_slots:
                slots_created.append(
                    TournamentSlot(
                        booking=booking,
                        date=final_date,
                        start_time=start,
                        end_time=end,
                        price=SLOT_PRICE,
                        status='SHIFTED' if final_date != current_date else 'BOOKED'
                    )
                )
        current_date += timedelta(days=1)

    return slots_created


# ----------------------------------
# CUSTOM PLAN (USER SELECTED DATES)
# ----------------------------------
def generate_custom_plan_slots(booking, selected_dates, start_hour, end_hour):
    """
    selected_dates: list of date objects
    """
    hour_slots = generate_hour_slots(start_hour, end_hour)
    slots_created = []

    for selected_date in selected_dates:
        final_date = (
            selected_date if not is_blocking_holiday(selected_date)
            else get_next_valid_date(selected_date, selected_date.weekday())
        )

        for start, end in hour_slots:
            slots_created.append(
                TournamentSlot(
                    booking=booking,
                    date=final_date,
                    start_time=start,
                    end_time=end,
                    price=SLOT_PRICE,
                    status='SHIFTED' if final_date != selected_date else 'BOOKED'
                )
            )

    return slots_created


# ----------------------------------
# MAIN ENGINE ENTRY POINT
# ----------------------------------
def create_booking_with_slots(
    *,
    user,
    plan_type,
    weekdays=None,
    selected_dates=None,
    start_hour,
    end_hour
):
    """
    Central booking creator (single source of truth)
    """

    booking = TournamentBooking.objects.create(
        user=user,
        plan_type=plan_type,
        start_date=date.today(),
        end_date=date.today(),
        total_slots=0,
        total_amount=0
    )

    if plan_type == 'BASIC':
        slots = generate_basic_plan_slots(
            booking, weekdays[0], start_hour, end_hour
        )

    elif plan_type == 'MONTHLY':
        slots = generate_monthly_plan_slots(
            booking, weekdays, start_hour, end_hour
        )

    elif plan_type == 'CUSTOM':
        slots = generate_custom_plan_slots(
            booking, selected_dates, start_hour, end_hour
        )

    else:
        raise ValueError("Invalid plan type")

    TournamentSlot.objects.bulk_create(slots)

    total_slots = len(slots)
    total_amount = total_slots * SLOT_PRICE

    booking.total_slots = total_slots
    booking.total_amount = total_amount
    booking.save()

    return booking
