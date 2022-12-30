from django.urls import path

from goals import views

urlpatterns = [
    path('goal_category/create', views.GoalsCategoryCreateView.as_view()),
    path('goal_category/list', views.GoalsListCategoryView.as_view()),
    path('goal_category/<int:pk>', views.GoalsCategoryView.as_view()),
]
