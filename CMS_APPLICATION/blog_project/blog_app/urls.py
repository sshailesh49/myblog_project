from django.urls import path,include
from . import views
urlpatterns = [
     # BlogAPI URLS - use "127.0.0.1:8000/blog/api/
     
     path('api/', views.BlogAPI.as_view()),
     path('api/<int:pk>/', views.BlogAPI.as_view()),
       
     #LikeAPI Urls - use "127.0.0.1:8000/blog/like/
     
     path('like/', views.LikeAPI.as_view()),
     path('like/<int:pk>/', views.LikeAPI.as_view()),
]