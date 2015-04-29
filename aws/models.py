from django.db import models
from django.contrib.auth.models import User
import json

# Create your models here.

class Awsaction(models.Model):
    user = models.OneToOneField(User)
    ins_id = models.CharField(max_length=255,unique=False)
    selected_action = models.TextField(max_length=128)
    date = models.DateTimeField()
    days = models.TextField(blank=True,max_length=200,unique=False)
    recurring = models.BooleanField(default=False)
    weeks = models.IntegerField(blank=True)

    def __unicode__(self):
        return self.ins_id

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    picture = models.ImageField(upload_to='profile_images', blank=True)
    awskey = models.TextField(max_length=128,blank=True)
    awssecret = models.TextField(max_length=128,blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
