from django.urls import path

from . import views

app_name = 'group'

urlpatterns = [
    path('', views.GetGroupsView.as_view(), name='list'),
    path('create/', views.CreateGroupView.as_view(), name='create'),
]