from django.db import models
from datetime import datetime, timedelta
from account.models.user import User
from account.models.professional import Professional
from django.urls import reverse
from django.utils import timezone
import pytz

israel_tz = pytz.timezone('Asia/Jerusalem')
now = timezone.now().astimezone(israel_tz)


class PriceList(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    job_name = models.CharField(max_length=120)
    price = models.PositiveIntegerField(null=False, blank=False)

    def __str__(self):
        return f'Professional: ({self.professional}). Job: {self.job_name}. Price: {self.price}'

    class Meta:
        db_table = 'PriceList'

    @staticmethod
    def get_type_of_jobs_by_professional(professional: int):
        return list(PriceList.objects.filter(professional=professional))

    @staticmethod
    def get_type_of_jobs_name_and_price_list(professional: int):
        type_of_jobs = PriceList.objects.filter(professional=professional)
        names_and_prices = type_of_jobs.values_list('job_name', 'price')
        return names_and_prices


class Appointment(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(PriceList, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    summary = models.TextField(blank=True)

    class Meta:
        db_table = 'Appointment'

    def __str__(self):
        return f'Professional: ({self.professional}). Client: ({self.user}). Time: {self.start} - {self.end}'

    @staticmethod
    def filter_appointments_from_now(user: User, user_type: bool):
        all_appointments_from_now = []
        if user_type is True:
            filtered_appointments_by_user = Appointment.objects.filter(professional=user)
        else:
            filtered_appointments_by_user = Appointment.objects.filter(user=user)
        for user_appointment in filtered_appointments_by_user:
            if user_appointment.start >= now:
                all_appointments_from_now.append(user_appointment)
        return all_appointments_from_now


class Schedule(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    start_day = models.DateTimeField()
    end_day = models.DateTimeField()
    meeting_time = models.PositiveIntegerField(null=False, blank=False)

    class Meta:
        db_table = 'Schedule'

    def __str__(self):
        professional = f'Professional: {self.professional}'
        starting = f'Starting: {self.start_day}'
        ending = f'Ending: {self.end_day}'
        meeting_time = f'Meeting time: {self.meeting_time}'
        return f'{professional}. {starting}. {ending}. {meeting_time}'

    @staticmethod
    def get_professional_possible_meetings(professional: Professional, day: int, month: int, year: int):
        professional_schedule_day = Schedule.objects.filter(
            professional=professional, start_day__day=day, start_day__month=month, start_day__year=year
        )
        meetings = []
        if professional_schedule_day:
            meeting_time = professional_schedule_day[0].meeting_time
            meetings = []
            start_time = datetime.combine(professional_schedule_day[0].start_day.date(),
                                          professional_schedule_day[0].start_day.time())
            end_time = datetime.combine(professional_schedule_day[0].end_day.date(),
                                        professional_schedule_day[0].end_day.time())
            while start_time + timedelta(minutes=meeting_time) <= end_time:
                meetings_str = f"{start_time.time().strftime('%H:%M')}-" \
                               f"{(start_time + timedelta(minutes=meeting_time)).time().strftime('%H:%M')}"
                meetings.append(meetings_str)
                start_time += timedelta(minutes=meeting_time)
        return meetings

    @staticmethod
    def get_free_meetings(professional: int, day: int, month: int, year: int):
        free_meetings = []
        meetings = Schedule.get_professional_possible_meetings(professional, day, month, year)
        for i, j in enumerate(meetings):
            start_meetings = meetings[i].split("-")[0]
            exists_appointment = Appointment.objects.filter(professional=professional,
                                                            start__day=day,
                                                            start__month=month,
                                                            start__year=year,
                                                            start__hour=int(start_meetings.split(":")[0]),
                                                            start__minute=int(start_meetings.split(":")[1]))
            if len(exists_appointment) == 0:
                free_meetings.append(meetings[i])

        return free_meetings

    @property
    def get_html_url(self):
        url = reverse("schedule_detail", args=(self.id,))
        start_time = self.start_day.strftime("%H:%M:%S")
        end_time = self.end_day.strftime("%H:%M:%S")
        return f'<a href="{url}"> {start_time} - {end_time} </a>'
