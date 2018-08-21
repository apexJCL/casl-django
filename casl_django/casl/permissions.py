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
