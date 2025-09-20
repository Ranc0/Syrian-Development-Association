from django.urls import path
from dashboard.views import UserListDashboardView , DashboardUserCreateView ,SignInView , DeleteUserByIdView , BeneficiaryUserListDashboardView , LogoutView , DashboardResetPasswordView , DashboardVerifyOTPView,DashboardForgotPasswordView

urlpatterns = [
    path('users/', UserListDashboardView.as_view(), name='dashboard-user-list'),
    path('users/beneficiary/', BeneficiaryUserListDashboardView.as_view(), name='dashboard-beneficiary-user-list'),

    path('users/create/', DashboardUserCreateView.as_view(), name='dashboard-user-create'),
    path('auth/signin/', SignInView.as_view(), name='user-signin'),
    path('users/delete/<int:user_id>/', DeleteUserByIdView.as_view(), name='delete-user'),
    path('users/password/forgot/', DashboardForgotPasswordView.as_view(), name='forgot-password'),
    path('users/password/confirm-otp/', DashboardVerifyOTPView.as_view(), name='confirm-reset-otp'),
    path('users/password/reset/', DashboardResetPasswordView.as_view(), name='reset-password'),
    path('users/logout/', LogoutView.as_view(), name='logout'),
]
