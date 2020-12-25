from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Twitter(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    positive_words = models.TextField(blank=True)
    negative_words = models.TextField(blank=True)



