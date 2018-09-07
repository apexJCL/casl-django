from django.db import models
from django.utils import timezone
from .casl import casl

from .config import config


class CASLPermissionQuerySet(models.QuerySet):
    def bundled(self) -> dict:
        """
        Groups the permissions by subject and returns them bundled.

        The dict keys are the subjects and the values are the actions

        :return:
        """
        rules = dict()
        for permission in self:
            if permission.subject not in rules:
                rules[permission.subject] = []
            rules[permission.subject].append(permission.action)
        return rules


class CASLPermissionManager(models.Manager):
    def get_queryset(self):
        return CASLPermissionQuerySet(self.model, using=self._db)


# Create your models here.
class CASLPermission(models.Model):
    objects = CASLPermissionManager()

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
            subject=self.subject,
            action=self.action
        )


class UserPermissionQuerySet(models.QuerySet):
    def bundled(self):
        return casl.merge_user_permissions(list(self))


class UserPermissionManager(models.Manager):
    def get_queryset(self):
        return UserPermissionQuerySet(self.model, using=self._db)


class UserPermission(models.Model):
    """
    Defines the permissions that an specific user has
    """
    objects = UserPermissionManager()

    class Meta:
        unique_together = ('permission', 'user')

    permission = models.ForeignKey('casl_django.CASLPermission', on_delete=models.CASCADE, help_text="Permission")
    user = models.ForeignKey(config.USER_MODEL, on_delete=models.CASCADE, help_text="User",
                             related_name="casl_permissions")
    created = models.DateTimeField(default=timezone.now, help_text="Created date")
