from django.contrib.auth.models import Permission, User

from casl_django.casl.casl import default_content_type_to_subject, default_permission_codename_to_action


def default_permission_to_casl_rule(permission: Permission) -> dict:
    """
    Given a default Django permission, converts the specified permission to a CASL config object

    :param permission: Permission to convert
    :return:
    """
    return {
        'subject': default_content_type_to_subject(permission.content_type),
        'action': default_permission_codename_to_action(permission)
    }


def default_permissions_to_casl_rule(permissions: list = None, subject: str = None) -> dict:
    """
    Given a list of permissions, return a rule that has all the actions specified for it.

    If no subject given, the default will be the first permission's content type

    :param permissions:
    :param subject:
    :return dict:
    """
    assert (permissions is not None), "Expected a list, got None"
    rule = dict()
    actions = []
    for permission in permissions:
        if not subject:
            subject = default_content_type_to_subject(permission.content_type)
        actions.append(default_permission_codename_to_action(permission))
    rule['subject'] = subject
    rule['actions'] = actions
    return rule


def casl_permissions_to_casl_rule(permissions: list = None, subject: str = None) -> list:
    """
    Given a list of CASLPermissions, return a rule that has all the actions specified for it

    :param permissions:
    :param subject:
    :return:
    """
    assert (permissions is not None), "Expected a list, got None"
    actions = []
    for permission in permissions:
        if not subject:
            subject = permission.subject
        actions.append(permission.action)
    return [{
        'subject': subject,
        'actions': actions
    }]


def django_permission_to_casl_rule(permission: Permission, subject: str = None):
    """
    Converts a permission to a casl rule

    :param permission:
    :param subject:
    :return:
    """
    rule = dict()
    rule['subject'] = subject if subject else default_content_type_to_subject(permission.content_type)
    rule['actions'] = default_permission_codename_to_action(permission)
    return rule


def get_user_inherited_permissions(user: User):
    """
    Returns all the permissions the user inherits by it's group

    :param user:
    :return:
    """
    perms = []
    for group in user.groups.all():
        perms += list(group.permissions.all())
    return perms
