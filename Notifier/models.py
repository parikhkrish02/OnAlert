from django.db import models


# Create your models here.


class Contest(models.Model):
    platform_img = models.ImageField(upload_to='notifier/images/', default='')
    platform = models.CharField(max_length=20)
    platform_link = models.CharField(max_length=200, default='')
    contest = models.CharField(max_length=50)
    contest_link = models.CharField(max_length=200)
    when = models.DateTimeField()
    duration = models.IntegerField(default=3)

    def __str__(self):
        return self.contest
