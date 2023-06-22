from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form

from account.forms import SignUpForm, LoginForm


def register(request):
    if request.method == 'GET':
        context = {'form': SignUpForm()}
        return render(request, 'account/register.html', context=context)
    elif request.method == 'POST':
        context = {'form': SignUpForm(request.POST)}
        if context['form'].is_valid():
            user = context['form'].save()
            messages.success(request, 'You have been registered successfully!')
            template = render(request, 'account/profile.html')
            template['Hx-Push'] = '/profile/'
            return template
        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form=context['form'], context=ctx)
        return HttpResponse(form_html)
    else:
        raise Http404


def check_phone(request):
    return generic_check(request=request, field='phone_number')


def check_password(request):
    return generic_check(request=request, field='password')


def check_first_name(request):
    return generic_check(request=request, field='first_name')


def check_last_name(request):
    return generic_check(request=request, field='last_name')


def check_country(request):
    return generic_check(request=request, field='country')


def check_city(request):
    return generic_check(request=request, field='city')


def generic_check(request, field):
    form = SignUpForm(request.GET)
    context = {
        'field': as_crispy_field(form[field]),
        'valid': not form[field].errors
    }
    return render(request, 'account/partials/field.html', context)



def sign_in(request):
    if request.method == 'GET':
        context = {'form': LoginForm()}
    elif request.method == 'POST':
        context = {'form': LoginForm(request.POST)}

        if context['form'].is_valid():
            username = context['form'].cleaned_data['username']
            password = context['form'].cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Hi {username.title()}, welcome back!')
                return redirect('profile_landing')

        messages.error(request, 'Invalid username or password')
    else:
        raise Http404
    return render(request, 'account/login.html', context)
