from django.urls import path
from ..views import (
    RegisterPendingUserView,
    ConfirmOTPView,
    LoginView,
    ProfileView,
    UpdateUserView,
    ForgotPasswordRequestView,
    ConfirmPasswordResetOTPView,
    ResetPasswordView,
    LogoutView
)

urlpatterns = [
    path('register/', RegisterPendingUserView.as_view(), name='register'),
    path('confirm-otp/', ConfirmOTPView.as_view(), name='confirm-otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', UpdateUserView.as_view(), name='profile-update'),
    path('password/forgot/', ForgotPasswordRequestView.as_view(), name='forgot-password'),
    path('password/confirm-otp/', ConfirmPasswordResetOTPView.as_view(), name='confirm-reset-otp'),
    path('password/reset/', ResetPasswordView.as_view(), name='reset-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
]