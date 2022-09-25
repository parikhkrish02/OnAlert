from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Contest(models.Model):
    platform_img = models.ImageField(upload_to="notifier/images/", default="")
    platform_name = models.CharField(max_length=20)
    platform_link = models.CharField(max_length=200, default="")
    contest = models.CharField(max_length=50)
    contest_link = models.CharField(max_length=200)
    when = models.DateTimeField()
    duration = models.IntegerField(default=3)

    def __str__(self):
        return self.contest


class Platform(models.Model):
    platform_name = models.CharField(max_length=20)
    platform_link = models.CharField(max_length=200, default="", blank=True)
    contest = models.ManyToManyField(Contest, blank=True)

    def __str__(self):
        return self.platform_name


class MyContest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    selectedContest = models.ManyToManyField(Platform, blank=True)

    def __str__(self):
        return self.user.username
