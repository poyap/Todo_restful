from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

    
class CustomUser(AbstractUser):
    ROLES = (
        (1, "Project Manager"),
        (2, "Developer"),
    )
    role = models.PositiveSmallIntegerField(choices=ROLES, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(CustomUser, self).save(*args, **kwargs)