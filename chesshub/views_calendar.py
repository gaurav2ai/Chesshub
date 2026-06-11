from datetime import date, datetime, timedelta, time
from calendar import monthrange
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from chesshub.models import Holiday


WORKING_START_HOUR = 10
WORKING_END_HOUR = 18


@login_required
def calendar_api(request):
    year = int(request.GET.get("year"))
    month = int(request.GET.get("month"))

    days_in_month = monthrange(year, month)[1]

    calendar_days = []

    for day in range(1, days_in_month + 1):
        current_date = date(year, month, day)

        holiday = Holiday.objects.filter(date=current_date).first()

        is_holiday = holiday is not None
        blocking = holiday.is_blocking() if holiday else False

        day_data = {
            "date": current_date.isoformat(),
            "weekday": current_date.strftime("%A"),
            "is_holiday": is_holiday,
            "holiday_name": holiday.name if holiday else None,
            "holiday_type": holiday.holiday_type if holiday else None,
            "blocking": blocking,
            "slots": []
        }

        if not blocking:
            for hour in range(WORKING_START_HOUR, WORKING_END_HOUR):
                day_data["slots"].append({
                    "start": f"{hour:02d}:00",
                    "end": f"{hour+1:02d}:00",
                    "status": "AVAILABLE"
                })

        calendar_days.append(day_data)

    return JsonResponse({
        "year": year,
        "month": month,
        "days": calendar_days
    })
