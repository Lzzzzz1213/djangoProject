from django.urls import path
from . import views

urlpatterns = [
    path('zhuce/', views.UserViewSet.as_view(), name='user_view_set'),
]