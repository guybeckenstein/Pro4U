from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from account.forms import UpdateForm
from account.models.professional import Professional
from reservation.models import PriceList
from review.models import Review


def landing(request):
    if request.user.is_authenticated:
        return render(request, 'account/profile.html')
    return render(request, 'landing/homepage.html')


@login_required
def settings(request):
    if request.user.is_authenticated:
        return render(request, 'account/profile_settings.html', {})
    return render(request, 'landing/homepage.html')


@login_required
def update_profile(request):
    if request.method == 'GET':
        context = {'form': UpdateForm(instance=request.user)}
        return render(request, 'account/update_profile.html', context=context)
    elif request.method == 'POST':
        context = {'form': UpdateForm(request.POST, request.FILES, instance=request.user)}
        if context['form'].is_valid():
            user = context['form'].save()
            messages.success(request, 'Updated profile successfully!')
            template = render(request, 'account/profile_settings.html')
            template['Hx-Push'] = reverse('profile_settings')
            return template
        return render(request, 'account/update_profile.html', context)
    else:
        raise Http404


def business_page(request, ID):
    if request.user.is_authenticated:
        professional = get_object_or_404(Professional, id=ID)
        type_of_jobs = PriceList.get_type_of_jobs_by_professional(professional=professional.id)
        # Reviews
        reviews = Review.filter_by_professional(professional=ID)
        one_star_reviews = reviews.filter(rating=Review.Rating.ONE_STAR[0])
        two_star_reviews = reviews.filter(rating=Review.Rating.TWO_STARS[0])
        three_star_reviews = reviews.filter(rating=Review.Rating.THREE_STARS[0])
        four_star_reviews = reviews.filter(rating=Review.Rating.FOUR_STARS[0])
        five_star_reviews = reviews.filter(rating=Review.Rating.FIVE_STARS[0])
        total_reviews = reviews.count()
        if total_reviews == 0:
            one_star_percent = 0
            two_star_percent = 0
            three_star_percent = 0
            four_star_percent = 0
            five_star_percent = 0
        else:
            one_star_percent = one_star_reviews.count() / total_reviews
            two_star_percent = two_star_reviews.count() / total_reviews
            three_star_percent = three_star_reviews.count() / total_reviews
            four_star_percent = four_star_reviews.count() / total_reviews
            five_star_percent = five_star_reviews.count() / total_reviews
        context = {
            'professional': professional,
            'type_of_jobs': type_of_jobs,
            'reviews': total_reviews,
            'ONE': one_star_reviews.count(),
            'TWO': two_star_reviews.count(),
            'THREE': three_star_reviews.count(),
            'FOUR': four_star_reviews.count(),
            'FIVE': five_star_reviews.count(),
            'ONE_PERCENT': one_star_percent * 100,
            'TWO_PERCENT': two_star_percent * 100,
            'THREE_PERCENT': three_star_percent * 100,
            'FOUR_PERCENT': four_star_percent * 100,
            'FIVE_PERCENT': five_star_percent * 100,
            'AVG': Review.get_professional_avg_rating(professional=ID)
        }
        return render(request, 'account/business_page.html', context)
    return render(request, 'landing/homepage.html')
