from django.urls import path

from core.views import UserRegistrationView, UserLoginView, UserProfileView, UserChangePasswordView

urlpatterns = [
    path('signup', UserRegistrationView.as_view(), name='signup'),
    path('login', UserLoginView.as_view(), name='login'),
    path('profile', UserProfileView.as_view(), name='profile'),
    path('update_password', UserChangePasswordView.as_view(), name='update-password')
]
