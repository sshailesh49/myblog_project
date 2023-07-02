from django.urls import path,include
from . import views



urlpatterns = [
    # UserAPI urls -- use "127.0.0.1:8000/user/api/"
    
    path('api/',views.UserAPI.as_view()),
    path('api/<int:pk>/',views.UserAPI.as_view())
]