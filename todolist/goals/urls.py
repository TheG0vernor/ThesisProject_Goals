from django.urls import path

from goals import views

urlpatterns = [
    path('goal_category/create', views.GoalsCategoryCreateView.as_view()),
    path('goal_category/list', views.GoalsListCategoryView.as_view()),
    path('goal_category/<int:pk>', views.GoalsCategoryView.as_view()),
    path('goal/create', views.GoalsCreateView.as_view()),
    path('goal/list', views.GoalsListView.as_view()),
    path('goal/<int:pk>', views.GoalsView.as_view()),
    path('goal_comment/create', views.GoalCommentCreateView.as_view()),
    path('goal_comment/list', views.GoalCommentListView.as_view()),
    path('goal_comment/<int:pk>', views.GoalCommentView.as_view()),
]
