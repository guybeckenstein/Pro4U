from datetime import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button
from django import forms
from account.models.user import User
from django.urls import reverse_lazy, reverse

from account.models.professional import Professional


class SignUpForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'register-form'
        self.helper.attrs = {
            'hx-post': reverse_lazy('register'),
            'hx-target': '#register-form',
            'hx-swap': 'outerHTML'
        }
        self.helper.add_input(Submit('submit', 'Submit'))

    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'max': datetime.now().date()}))
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('phone_number', 'email', 'password', 'date_of_birth', 'type',
                  'first_name', 'last_name', 'country', 'city', 'address')
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'hx-get': reverse_lazy('check-phone'),
                'hx-trigger': "keyup changed delay:.5s",
                'hx-target': '#div_id_phone_number',
                'placeholder': 'Phone Number (username)',
            }),
            'password': forms.PasswordInput(attrs={
                'hx-get': reverse_lazy('check-password'),
                'hx-target': '#div_id_password',
                'placeholder': 'Password',
            }),
            'type': forms.RadioSelect(),
            'first_name': forms.TextInput(attrs={
                'hx-get': reverse_lazy('check-first-name'),
                'hx-trigger': "keyup changed delay:.5s",
                'hx-target': '#div_id_first_name',
                'placeholder': 'First Name',
            }),
            'last_name': forms.TextInput(attrs={
                'hx-get': reverse_lazy('check-last-name'),
                'hx-trigger': "keyup changed delay:.5s",
                'hx-target': '#div_id_last_name',
                'placeholder': 'Last Name',
            }),
            'country': forms.TextInput(attrs={
                'hx-get': reverse_lazy('check-country'),
                'hx-trigger': "keyup changed delay:.5s",
                'hx-target': '#div_id_country',
                'placeholder': 'Country',
            }),
            'city': forms.TextInput(attrs={
                'hx-get': reverse_lazy('check-city'),
                'hx-trigger': "keyup changed delay:.5s",
                'hx-target': '#div_id_city',
                'placeholder': 'City',
            }),
        }

    def clean_phone_number(self):
        phone_number: str = self.cleaned_data['phone_number']
        if phone_number.isnumeric() is False:
            raise forms.ValidationError('Phone number cannot contain characters')
        elif len(phone_number) < 9:
            raise forms.ValidationError('Phone number is too short')
        elif len(phone_number) > 12:
            raise forms.ValidationError('Phone number is too long')
        self.cleaned_data['username'] = phone_number
        return phone_number

    def clean_password(self):
        password: str = self.cleaned_data['password']
        count_uppercase = 0
        count_lowercase = 0
        count_numeric = 0
        count_special = 0
        for c in password:
            if 'A' <= c <= 'Z':
                count_uppercase += 1
            elif 'a' <= c <= 'z':
                count_lowercase += 1
            elif '0' <= c <= '9':
                count_numeric += 1
            else:
                count_special += 1
        if len(password) < 8:
            raise forms.ValidationError('Password is too short')
        elif count_uppercase == 0:
            raise forms.ValidationError('Password must contain uppercase letter')
        elif count_lowercase == 0:
            raise forms.ValidationError('Password must contain lowercase letter')
        elif count_numeric == 0:
            raise forms.ValidationError('Password must contain numeric letter')
        elif count_special == 0:
            raise forms.ValidationError('Password must contain special letter')
        return password

    def clean_first_name(self):
        return self.validate(attribute_value='first_name', attribute_string='First name')

    def clean_last_name(self):
        return self.validate(attribute_value='last_name', attribute_string='Last name')

    def clean_country(self):
        return self.validate(attribute_value='country', attribute_string='Country')

    def clean_city(self):
        return self.validate(attribute_value='city', attribute_string='City')

    def validate(self, attribute_value: str, attribute_string: str):
        cleaned: str = self.cleaned_data[attribute_value]
        if cleaned is None:
            forms.ValidationError(f'{attribute_string} is invalid')
        elif all(c.isalpha() or c.isspace() for c in list(cleaned)):
            return cleaned
        else:
            raise forms.ValidationError(f'{attribute_string} can only contain characters')

    def save(self, commit=True):
        """ Hash user's password on save """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(
        max_length=32, widget=forms.PasswordInput, required=True, min_length=6
    )

    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'password': forms.PasswordInput()
        }


class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone_number', 'email', 'image', 'date_of_birth',
                  'first_name', 'last_name', 'country', 'city', 'address')
        widgets = {
            'date_of_birth': forms.DateInput(),
            'image': forms.FileInput(attrs={'multiple': False}),
        }
        labels = {
            'phone_number': 'Phone number (view-only)'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('profile_edit')
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Update', css_class='btn-dark'))
        redirect_url = reverse('profile_settings')
        self.helper.add_input(Button(
            'redirect',
            'Back to settings',
            css_class='btn-warning',
            onclick=f'window.location.href="{redirect_url}";'
        ))
        self.fields['image'].required = False  # Make the image field optional
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['phone_number'].widget.attrs['readonly'] = True

    def clean_phone_number(self):
        if self.instance:
            return self.instance.phone_number
        else:
            return self.fields['phone_number']

    # def save(self, commit=True):
    #     """ Hash user's password on save """
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data['password'])
    #     if commit:
    #         user.save()
    #     return user

# TODO: add ProfessionalCreateForm, ProfessionalUpdateForm
# class ProfessionalUpdateForm(forms.ModelForm):
#
#     class Meta:
#         model = Professional
