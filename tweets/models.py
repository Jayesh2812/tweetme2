from django.db import models
import random
# Create your models here.
class Tweet(models.Model):
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', null=True, blank=True)
    class Meta:
        ordering=["-id"]

    def __str__(self):
        return f"{self.id} -> {self.content}"

    def serialize(self):
        return{
            "id" : self.id,
            "content" : self.content,
            "likes" : random.randint(0, 100)
        }