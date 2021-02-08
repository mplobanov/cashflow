from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import datetime


# Create your models here.

class User_info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.IntegerField()

    def __str__(self):
        return str(self.user.username) + " " + str(self.money) + "CR"

class Cheque(models.Model):
    amount = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    sequrity_code = models.IntegerField(default=11111, unique=True)
    activated = models.BooleanField()

    def __str__(self):
        return "{} cheque from {} for {} CR".format("Activated" if self.activated else "Not activated", self.author.username, self.amount)

class HistoryNote(models.Model):
    date = models.DateTimeField(default=datetime(2000, 1, 1, 12, 0, 0, 0))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return "{} note: {}".format(self.user.username, self.text)


