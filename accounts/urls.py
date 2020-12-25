from django.urls import path

from .views import (
    LogInView, ResendActivationCodeView, RemindUsernameView, SignUpView, ActivateView,
    ChangeEmailView, ChangeEmailActivateView, ChangePasswordView,
    RestorePasswordView, RestorePasswordConfirmView, Logout, ChangeEmailView2, ChangePasswordView2,
    ChangeUserView,
)

app_name = 'accounts'

urlpatterns = [
    path('log-in/', LogInView.as_view(), name='log_in'),
    path('log-out/', Logout, name='log_out'),
    path('resend/activation-code/', ResendActivationCodeView.as_view(), name='resend_activation_code'),
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('activate/<code>/', ActivateView.as_view(), name='activate'),
    path('restore/password/', RestorePasswordView.as_view(), name='restore_password'),
    path('restore/<uidb64>/<token>/', RestorePasswordConfirmView.as_view(), name='restore_password_confirm'),
    path('remind/username/', RemindUsernameView.as_view(), name='remind_username'),
    path('change/password/', ChangePasswordView.as_view(), name='change_password'),
    path('change/email/', ChangeEmailView.as_view(), name='change_email'),
    path('change/email/', ChangeEmailView.as_view(), name='change_email'),
    path('change/username/', ChangeUserView.as_view(), name='change_username'),
    path('dashboard/email/', ChangeEmailView2.as_view(), name='change_email'),
    path('dashboard/password/', ChangePasswordView2.as_view(), name='change_password'),
    path('change/email/<code>/', ChangeEmailActivateView.as_view(), name='change_email_activation'),
]
