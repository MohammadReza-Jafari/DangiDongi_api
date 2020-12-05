from django.urls import path, include, reverse

from . import views

app_name = 'user'
urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('get-token/', views.LoginUserView.as_view(), name='get-toke'),
    path('profile/', views.GetProfileView.as_view(), name='profile')
]