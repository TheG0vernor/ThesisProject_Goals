from django.urls import path

from goals import views

urlpatterns = [
    path('goal_category/create', views.GoalsCategoryCreateView.as_view()),
    path('goal_category/list', views.GoalsCategoryListView.as_view()),
    path('goal_category/<int:pk>', views.GoalsCategoryView.as_view()),
    path('goal/create', views.GoalsCreateView.as_view(), name='goal_create'),
    path('goal/list', views.GoalsListView.as_view()),
    path('goal/<int:pk>', views.GoalsView.as_view()),
    path('goal_comment/create', views.GoalCommentCreateView.as_view()),
    path('goal_comment/list', views.GoalCommentListView.as_view()),
    path('goal_comment/<int:pk>', views.GoalCommentView.as_view()),
    path('board/create', views.BoardCreateView.as_view(), name='board_create'),
    path('board/list', views.BoardListView.as_view(), name='board_list'),
    path('board/<int:pk>', views.BoardView.as_view(), name='board'),
]
