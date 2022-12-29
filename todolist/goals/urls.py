from django.urls import path

from goals import views

urlpatterns = [
    path('goal_category/create', views.GoalsCategoryCreateView.as_view()),
]
