from django.shortcuts import render
from django.http import HttpResponse
from .models import AdGeneration
from .serializers import AdGeneratorSerializer
from rest_framework import generics
from .tasks import generate_task

class AdGeneratorAPI(generics.ListCreateAPIView):
    queryset=AdGeneration.objects.all()
    serializer_class=AdGeneratorSerializer
    def perform_create(self, serializer):
        instance=serializer.save()
        generate_task.delay(instance.id)
class RetrieveAPI(generics.RetrieveAPIView):
    queryset=AdGeneration.objects.all()
    serializer_class=AdGeneratorSerializer

        



# Create your views here.
