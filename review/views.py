from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect

from account.models.user import User
from account.models.professional import Professional
from .forms import ReviewForm
from .models import Review


class UnauthenticatedUser404Mixin(UserPassesTestMixin):
    """
    `UserPassesTestMixin` checks whether the user is authenticated or not. If the user is
    authenticated, they will be allowed to access the view. If not, `test_func` will return
    false and handle the `handle_no_permission` method will be called, which returns a 404 response.

    This class will be inherited by all other classes in `views.py`
    """
    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return HttpResponseNotFound()


class ReviewListView(LoginRequiredMixin, UnauthenticatedUser404Mixin, ListView):
    model = Review
    context_object_name = 'reviews'
    paginate_by = 10

    def get_queryset(self):
        professional = get_object_or_404(Professional, id=self.kwargs['ID'])
        # Sort reviews if user pressed one of the buttons
        sort_by = self.request.GET.get('sort_by')
        # All sorting types use Review.objects to call ReviewManager method
        if sort_by == 'newest':
            queryset = Review.objects.sort_review_by_newest(professional=professional)
        elif sort_by == 'oldest':
            queryset = Review.objects.sort_review_by_oldest(professional=professional)
        elif sort_by == 'highest':
            queryset = Review.objects.sort_review_by_highest_rating(professional=professional)
        elif sort_by == 'lowest':
            queryset = Review.objects.sort_review_by_lowest_rating(professional=professional)
        else:
            queryset = Review.filter_by_professional(professional=professional).order_by('-description')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Enables sorting
        context['sort_by'] = self.request.GET.get('sort_by', '')
        context['professional'] = Professional.objects.get(id=self.kwargs['ID'])

        reviews = Review.filter_by_professional(professional=context['professional'])
        if reviews.count() > 0:
            context['review_count'] = reviews.count()
            avg_rating = Review.get_professional_avg_rating(professional=context['professional'])
            if avg_rating is not None:
                context['avg_rating'] = round(avg_rating, 2)
            else:
                context['avg_rating'] = 'N/A'

        # Filter by the user review if they are logged in
        if self.request.user.is_authenticated:
            # TODO: validate that it have had reservation with the professional before
            # TODO: fix after changed models in `account` app
            # Retrieving client ID
            user, _ = User.objects.get_or_create(id=self.request.user.id)
            if reviews.filter(user=user):
                context['user_review'] = True
            else:
                context['user_review'] = False

        return context


class ReviewCreateView(LoginRequiredMixin, UnauthenticatedUser404Mixin, CreateView):
    model = Review
    form_class = ReviewForm

    # In case user already reviewed the professional, this function redirects it to UpdateView instead of CreateView
    def dispatch(self, request, *args, **kwargs):
        # Retrieving client ID
        user, _ = User.objects.get_or_create(id=self.request.user.id)

        # Retrieving professional ID
        professional = self.kwargs['ID']

        # Check if the client has already reviewed the professional
        if Review.objects.filter(user=user, professional=professional).exists():
            # Client has already reviewed the professional, redirect them to the update page
            return redirect(reverse('review-update', kwargs={'ID': professional.id}))

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Retrieving client ID
        user, _ = User.objects.get_or_create(id=self.request.user.id)
        form.instance.user = user
        # Retrieving professional ID
        form.instance.professional = Professional.objects.get(id=self.kwargs['ID'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # This enables to see what is the name of the professional in the HTML template title
        context = super().get_context_data(**kwargs)
        context['professional'] = Professional.objects.get(id=self.kwargs['ID'])
        return context

    def get_success_url(self):
        return reverse('reviews', args=[self.kwargs['ID']])


class ReviewUpdateView(LoginRequiredMixin, UnauthenticatedUser404Mixin, UpdateView):
    model = Review
    form_class = ReviewForm

    def get_initial(self):
        initial = super().get_initial()
        # Retrieve the client ID (current user ID)
        user, _ = User.objects.get_or_create(user=self.request.user)
        initial['user'] = user
        return initial

    def get_object(self, queryset=None) -> Review:
        # Retrieve the review object based on Client ID (current session)
        user = self.request.user
        professional = self.kwargs['ID']
        reviews_by_client = Review.objects.filter(user=user, professional=professional).first()
        if reviews_by_client:
            filtered_review_id = reviews_by_client.id
        else:
            # Invalid input, then we will deliberately get 404 to see error
            filtered_review_id = -1
        review = get_object_or_404(Review, id=filtered_review_id, user=user)
        return review

    def get_context_data(self, **kwargs):
        # This enables to see what is the name of the professional in the HTML template title
        context = super().get_context_data(**kwargs)
        context['professional'] = Professional.objects.get(professional=self.kwargs['ID'])
        return context

    def get_success_url(self):
        return reverse('reviews', args=[self.kwargs['ID']])

    def test_func(self):
        # Only client X can update reviews of client X
        review = self.get_object()
        user, _ = User.objects.get_or_create(id=self.request.user.id)
        return user == review.user
