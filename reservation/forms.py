from django.forms import ModelForm, DateInput
from .models import Schedule
from django import forms
from django.core.validators import MinValueValidator


class PriceListForm(forms.Form):
    job_name = forms.CharField(max_length=120, required=True)
    price = forms.IntegerField(validators=[MinValueValidator(0)], required=True)


class ScheduleForm(ModelForm):
    class Meta:
        model = Schedule
        fields = ["start_day", "end_day", "meeting_time"]
        widgets = {

            "start_day": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_day": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "meeting_time": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Enter a positive number"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)
        self.fields["start_day"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_day"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields['meeting_time'].validators.append(MinValueValidator(0))
