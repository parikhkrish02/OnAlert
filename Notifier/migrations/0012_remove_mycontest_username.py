# Generated by Django 4.1 on 2022-09-17 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Notifier", "0011_mycontest_username"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mycontest",
            name="userName",
        ),
    ]