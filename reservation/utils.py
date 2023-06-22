from calendar import HTMLCalendar
from reservation.models import Schedule
from django.urls import reverse
from datetime import date
from django.utils import timezone
import pytz

israel_tz = pytz.timezone('Asia/Jerusalem')
now = timezone.now().astimezone(israel_tz)


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, professional_id=None, user=None):
        self.year = year
        self.month = month
        self.professional_id = professional_id
        self.user = user
        super(Calendar, self).__init__()

    def formatday(self, day, schedule):
        if self.user is False:
            schedule_per_day = schedule.filter(start_day__day=day)
        else:
            schedule_per_day = Schedule.get_professional_possible_meetings(self.professional_id, day, self.month, self.year)
        d = ""
        for schedule in schedule_per_day:
            if self.user is False:
                if schedule.start_day.day < now.day:
                    start_time = schedule.start_day.strftime("%H:%M:%S")
                    end_time = schedule.end_day.strftime("%H:%M:%S")
                    d += f"<li> {start_time} - {end_time}  </li>"
                else:
                    d += f"<li>  {schedule.get_html_url}  </li>"
            else:
                date_in_calendar = date(self.year, self.month, day)
                if date_in_calendar < now.date() or \
                        (date_in_calendar == now.date() and int(schedule.split(':')[0]) < now.hour) or \
                        (date_in_calendar == now.date() and int(schedule.split(':')[0]) == now.hour
                         and int(schedule.split(':')[1].split('-')[0]) < now.minute)\
                        or schedule not in Schedule.get_free_meetings(self.professional_id, day, self.month, self.year):
                    d += f"<li> {schedule}</li>"
                else:
                    url = reverse("confirm_appointment",
                                  args=[self.professional_id, day, self.month, self.year, schedule])
                    d += f'<a href="{url}"> {schedule},</a>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return "<td></td>"

    def formatweek(self, theweek, schedule):
        week = ""
        for d, weekday in theweek:
            week += self.formatday(d, schedule)
        return f"<tr> {week} </tr>"

    def formatmonth(self, withyear=True):
        schedule = Schedule.objects.filter(
            professional_id=self.professional_id,
            start_day__year=self.year, start_day__month=self.month
        )
        cal = (
            '<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        )  # noqa
        cal += (
            f"{self.formatmonthname(self.year, self.month, withyear=withyear)}\n"
        )  # noqa
        cal += f"{self.formatweekheader()}\n"
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f"{self.formatweek(week, schedule)}\n"
        return cal
