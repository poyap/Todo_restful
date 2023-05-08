from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    ROLES = (
        (1, "Project Manager"),
        (2, "Developer"),
    )
    role = models.PositiveSmallIntegerField(choices=ROLES)
    