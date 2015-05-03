from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128, blank=True)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    

    def __unicode__(self):
        return self.user.username

    def getUsername(self):
        return self.user.username

    def getEmail(self):
        return self.user.email
