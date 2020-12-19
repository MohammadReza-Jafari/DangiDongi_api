from django.urls import path

from wallet import views


app_name='wallet'
urlpatterns = [
    path('charge/', views.ChargeWalletView.as_view(), name='charge')
]