from rest_framework import serializers
from .models import AdGeneration
class AdGeneratorSerializer(serializers.ModelSerializer):
    class Meta:
        model=AdGeneration
        fields=['id','product_name','description','audience','platform','tone','duration','status']
    def create(self,data):
        instance=AdGeneration.objects.create(**data)
        return instance