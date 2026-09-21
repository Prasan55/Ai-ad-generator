from django.urls import path
from . import views

urlpatterns = [
    path('api/adgen/',views.AdGeneratorAPI.as_view()),
    path('api/retrieve/<int:pk>',views.RetrieveAPI.as_view()) 
]