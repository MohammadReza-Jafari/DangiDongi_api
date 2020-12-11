from django.urls import path, include, reverse

from . import views

app_name = 'user'
urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('get-token/', views.LoginUserView.as_view(), name='get-toke'),
    path('me/', views.GetProfileView.as_view(), name='profile'),
    path('activate/<str:code>/', views.ActivateUserView.as_view(), name='activation'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('get-reset-code/', views.GetResetCodeView.as_view(), name='get_reset_code'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password')
]