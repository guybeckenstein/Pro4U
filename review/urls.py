from django.urls import path
from . import views
from .models import Review

urlpatterns = [
    path('professional/<int:ID>/reviews/', views.ReviewListView.as_view(model=Review, paginate_by=10), name='reviews'),
    path('professional/<int:ID>/reviews/new/', views.ReviewCreateView.as_view(), name='review-create'),
    path('professional/<int:ID>/reviews/update/', views.ReviewUpdateView.as_view(), name='review-update'),
]
