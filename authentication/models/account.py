from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models

from template.models.common import TimestampedModel


class Account(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid4)
    email = models.CharField(max_length=128)
    is_verified = models.BooleanField(default=False)
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)

    @property
    def password(self) -> str:
        return self.user.password

    @property
    def username(self) -> str:
        return self.user.username

    def __str__(self):
        return f'Account: {self.email}'
