# Generated by Django 4.1 on 2022-09-17 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Notifier", "0010_alter_mycontest_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="mycontest",
            name="userName",
            field=models.CharField(default="", max_length=50),
        ),
    ]
