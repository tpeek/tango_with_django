from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    #username = models.CharField(max_length=128, unique=True)
    #firstName = models.CharField(max_length=128)
    #lastName = models.CharField(blank=True)
    #email = models.EmailField(blank=True)

    def __unicode__(self):
        return self.user.username

    def getUsername(self):
        return self.user.username

    def getWebsite(self):
        return self.user.website

    def getEmail(self):
        return self.user.email
    
    def delete(self):
        self = None
