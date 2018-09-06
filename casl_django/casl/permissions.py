from django.contrib.auth.models import AbstractUser

from .converter import Converter
from ..models import CASLPermission


class Permissions:
    @classmethod
    def default_permissions(cls):
        """
        Returns the default defined permissions on Django Permissions

        :return:
        """
        return Converter.default_permissions()

    @classmethod
    def custom_permissions(cls):
        """
        Returns the default custom permissions queryset implemented on Django
        :return:
        """
        return CASLPermission.objects.all()

    @classmethod
    def create(cls, subject: str, action: str):
        return CASLPermission.objects.create(subject=subject, action=action)

    @classmethod
    def permissions_for_user(cls, user, **kwargs):
        return CASLPermission.objects.filter(userpermission__user=user, **kwargs)

    @classmethod
    def set_user_permission(cls, user, permission: CASLPermission):
        return permission.userpermission_set.create(
            user=user
        )

    @classmethod
    def get_user_django_permissions(cls, user: AbstractUser = None):
        """
        Converts the user permission's to CASL-like rules.

        You can restrict the result given the permissions based on the model, group or directly assigned level.

        :param user: User
        :return:
        """
        perms = {}
        for group in user.groups.all():
            for permission in group.permissions.all():
                if permission.content_type not in perms:
                    perms[permission.content_type] = []
                perms[permission.content_type].append(permission)
        for permission in user.user_permissions.all():
            if permission.content_type not in perms:
                perms[permission.content_type] = []
            perms[permission.content_type].append(permission)
        return Converter.serialize_django_permissions(perms)
