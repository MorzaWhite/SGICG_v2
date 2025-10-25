from datetime import datetime, timedelta, time
from django.utils import timezone
from django.conf import settings
from certificacion.models import Orden

def calculate_delivery_date(start_date):
    """
    Calculates the suggested delivery date based on business hours
    and configured processing times.
    """
    business_hours = {
        0: (time(9, 0), time(17, 30)),  # Monday
        1: (time(9, 0), time(17, 30)),  # Tuesday
        2: (time(9, 0), time(17, 30)),  # Wednesday
        3: (time(9, 0), time(17, 30)),  # Thursday
        4: (time(9, 0), time(17, 30)),  # Friday
        5: (time(9, 0), time(13, 0)),   # Saturday
    }  # Sunday is closed

    total_hours = sum(settings.TIEMPOS_ETAPA.values())
    current_date = start_date
    hours_added = 0

    while hours_added < total_hours:
        weekday = current_date.weekday()

        if weekday in business_hours:
            day_start, day_end = business_hours[weekday]

            # If current time is before business hours, move to the start of the day
            if current_date.time() < day_start:
                current_date = current_date.replace(hour=day_start.hour, minute=day_start.minute)

            # If current time is after business hours, move to the next day
            if current_date.time() >= day_end:
                current_date += timedelta(days=1)
                current_date = current_date.replace(hour=business_hours.get(current_date.weekday(), (time(9,0),time(17,30)))[0].hour, minute=0, second=0)
                continue

            end_of_day_datetime = datetime.combine(current_date.date(), day_end)
            if timezone.is_aware(current_date):
                end_of_day_datetime = timezone.make_aware(end_of_day_datetime, current_date.tzinfo)

            time_left_in_day = (end_of_day_datetime - current_date).total_seconds() / 3600
            hours_to_add_today = min(time_left_in_day, total_hours - hours_added)

            current_date += timedelta(hours=hours_to_add_today)
            hours_added += hours_to_add_today

        else: # It's a Sunday
            current_date += timedelta(days=1)
            current_date = current_date.replace(hour=business_hours[0][0].hour, minute=0, second=0)

    return current_date
