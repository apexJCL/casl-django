from django.contrib.auth.models import ContentType

from .utils import default_permissions_to_casl_rule, casl_permissions_to_casl_rule


class Converter(object):
    @staticmethod
    def default_permissions():
        rules = []
        for content_type in ContentType.objects.all():
            rule = default_permissions_to_casl_rule(content_type.permission_set.all())
            rules.append(rule)
        return rules

    @staticmethod
    def serialize_django_permissions(permissions: dict):
        """
        Given a dict of django permissions, the dict must be

        {
            Content-Type: [Permission, Permission]
        }

        :param permissions: List of permissions
        :param bundled: If the rules must be bundled, ex: subject: 'payments', actions: ['add', 'cancel', 'change']
        :return:
        """
        rules = []
        for content_type, permissions in permissions.items():
            rules.append(default_permissions_to_casl_rule(permissions))
        return rules

    @staticmethod
    def serialize_rules(permissions, bundled: bool = True):
        """
        Given a queryset of CASLPermissions, return a list
        of them

        :param bundled:  If the rules should be returned compacted or expanded
        :param permissions:
        :return:
        """
        if bundled:
            return casl_permissions_to_casl_rule(permissions)
        rules = []
        for permission in permissions:
            rules.append(permission.as_rule)
        return rules
