from django.db import models
from django.utils import timezone

from .config import config


# Create your models here.
class CASLPermission(models.Model):
    class Meta:
        unique_together = ('subject', 'action')

    subject = models.CharField(max_length=config.SUBJECT_MAX_LENGTH, help_text="Subject")
    action = models.TextField(max_length=config.ACTION_MAX_LENGTH, help_text="Action")

    @property
    def as_rule(self):
        return {
            'subject': self.subject,
            'action': self.action
        }

    def __str__(self):
        return "{subject} -> {action}".format(
            subject=self.subject.capitalize(),
            action=self.action
        )


class UserPermission(models.Model):
    """
    Defines the permissions that an specific user has
    """

    class Meta:
        unique_together = ('permission', 'user')

    permission = models.ForeignKey('casl_django.CASLPermission', on_delete=models.CASCADE, help_text="Permission")
    user = models.ForeignKey(config.USER_MODEL, on_delete=models.CASCADE, help_text="User")
    created = models.DateTimeField(default=timezone.now, help_text="Created date")
