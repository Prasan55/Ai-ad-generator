from django.db import models
from django.contrib.auth.models import User
class AdGeneration(models.Model):
    audiences=[
        ("students","students"),
        ("business","business"),
        ("professional","professional")
    ]
    platforms=[("instagram","instagram"),("ytshorts","ytshorts"),("tiktok","tiktok")]
    product_name=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    audience=models.CharField(max_length=20,choices=audiences)
    platform=models.CharField(max_length=20,choices=platforms)
    tone=models.CharField(max_length=20)
    duration=models.IntegerField()
    status=models.CharField(max_length=20,default="pending",choices=[("pending","pending"),("completed","completed"),("failed","failed")])
    created_at=models.DateField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="adobjects",null=True)

    def __str__(self):
        return self.product_name
# Create your models here.
