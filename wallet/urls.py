from django.urls import path

from wallet import views


urlpatterns = [
    path('test/', views.TestView.as_view(), name='test')
]