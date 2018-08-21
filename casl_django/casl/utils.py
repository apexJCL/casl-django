from django.contrib.auth.models import Permission, ContentType


def _default_content_type_to_subject(content_type: ContentType) -> str:
    """
    Given a permission with a content type, define the subject naming convention.

    Ex:

    App called "products" and your model is called "item",
    this will create a subject called 'products/item'

    :param content_type:
    :return:
    """
    return "{app_label}/{model}".format(
        app_label=content_type.app_label,
        model=content_type.model
    )


def _default_permission_codename_to_action(permission: Permission) -> str:
    """
    Given an standard Django permission, return the action that has been specified to it

    :param permission:
    :return:
    """
    return permission.codename[:permission.codename.find('_')]


def default_permission_to_casl_rule(permission: Permission) -> dict:
    """
    Given a default Django permission, converts the specified permission to a CASL config object

    :param permission: Permission to convert
    :return:
    """
    return {
        'subject': _default_content_type_to_subject(permission.content_type),
        'action': _default_permission_codename_to_action(permission)
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
            subject = _default_content_type_to_subject(permission.content_type)
        actions.append(_default_permission_codename_to_action(permission))
    rule['subject'] = subject
    rule['actions'] = actions
    return rule
