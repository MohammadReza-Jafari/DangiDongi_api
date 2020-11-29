from django.urls import path, include

from . import views

app_name = 'user'
urlpatterns = [
    path('identity/', include([
        path('register/', views.RegisterUser.as_view(), name='register'),
    ]))
]