from django.contrib.auth.models import Permission, ContentType


def dict_to_casl_rules(rules: dict):
    """
    Given a dict where the keys are the subject and the values are the actions, return
    a list of dicts ready to be serialized as JSON

    :return:
    """
    perms = []
    for key, actions in rules.items():
        perms.append({
            'subject': key,
            'actions': actions
        })
    return perms


def default_content_type_to_subject(content_type: ContentType) -> str:
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


def default_permission_codename_to_action(permission: Permission) -> str:
    """
    Given an standard Django permission, return the action that has been specified to it

    :param permission:
    :return:
    """
    return permission.codename[:permission.codename.rfind('_')]


def django_permissions_to_casl_rules(permissions: list) -> list:
    """
    Given a list of permission objects, return casl rules

    :param permissions:
    :return:
    """
    rules = {}
    for permission in permissions:
        content_type = default_content_type_to_subject(permission.content_type)
        if content_type not in rules:
            rules[content_type] = []
        rules[content_type].append(default_permission_codename_to_action(permission))
    return dict_to_casl_rules(rules)


def merge_user_permissions(user_permissions: list):
    """
    Merges the list of user_permissions into a bundled action representation

    :param user_permissions:
    :return:
    """
    rules = dict()
    for user_permission in user_permissions:
        if user_permission.permission.subject not in rules:
            rules[user_permission.permission.subject] = []
        rules[user_permission.permission.subject].append(user_permission.permission.action)
    return dict_to_casl_rules(rules)
