from django.db import models
from django.contrib.auth.models import User

class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, null=False, help_text="Enter Name")

    def __str__(self) -> str:
        return self.name