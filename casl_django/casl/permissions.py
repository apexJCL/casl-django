from casl_django.casl import casl, utils


class Permissions:
    @staticmethod
    def user_permissions(user, django_perms_filter: dict = None, casl_permissions_filter: dict = None) -> list:
        """
        Given a user, return all of their permissions as casl-rule-style dicts.

        The list will contain dicts shaped as the casl object.

        [{subject: 'something', actions: ['a1', 'a2', 'a3']}]

        :param user: User
        :param django_perms_filter: Filtering options for the django permissions queryset
        :param casl_permissions_filter: Filtering options for the casl permissions queryset

        :return:
        """
        if not django_perms_filter:
            django_perms_filter = dict()
        if not casl_permissions_filter:
            casl_permissions_filter = dict()

        # List
        user_direct_permissions = casl.django_permissions_to_casl_rules(
            user.user_permissions.filter(**django_perms_filter)
        )
        # List 2
        user_inherited_permissions = casl.django_permissions_to_casl_rules(utils.get_user_inherited_permissions(user))

        # List 3
        user_casl_permissions = user.casl_permissions.filter(**casl_permissions_filter).bundled()
        return user_direct_permissions + user_inherited_permissions + user_casl_permissions
