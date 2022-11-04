from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Platform(models.Model):
    platform_name = models.CharField(max_length=20)
    platform_link = models.CharField(max_length=200, default="", blank=True)
    platform_img = models.ImageField(upload_to="notifier/images/", default="")

    def __str__(self):
        return self.platform_name


class Contest(models.Model):
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    contest = models.CharField(max_length=50)
    contest_link = models.CharField(max_length=200)
    when = models.DateTimeField()
    duration=models.CharField(max_length=20)

    def __str__(self):
        return self.contest


class MyContest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    selectedContest = models.ManyToManyField(Platform, blank=True)

    def __str__(self):
        return self.user.username
