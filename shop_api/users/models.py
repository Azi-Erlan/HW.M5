from django.db import models
from django.contrib.auth.models import User


class ConfirmationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)

    def __str__(self):
        return f'{self.user.username} - {self.code}'