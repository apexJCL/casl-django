===========
CASL-Django
===========

CASL Django is an app that converts the usual Django permissions to CASL-Style rules.


CASL is an isomorphic authorization JavaScript library:
https://github.com/stalniy/casl/

Example
-------

Having a rule called **my_app.change_item**, will generate a CASL rule:

::

    {
        subject: 'my_app/item',
        action: 'change'
    }


If you have more than one rule for the same subject, for example:

::

    my_app.change_item
    my_app.add_item
    my_app.remove_item

This will generate:

::

    {
        subject: 'my_app/item',
        actions: ['add', 'change', 'remove']
    }

Configuration
-------------

By default, the length for subject and action fields is 128 characters, you can
increase the length of them by adding to your settings file:

::

    CASL_DJANGO = {
        'subject-length': 256,
        'action-length': 256
    }

Custom Permissions
------------------

Sometimes you'd like to have custom permissions for your users, given this, you
can add to your user using the Permission's `add_permission` class method::

    from casl_django.casl.permissions import Permissions

    ...

    my_custom_permission = Permissions.create(subject="navigation", action="index")

    ...

    Permissions.set_user_permission(user=user, permission=my_custom_permission)


Or you can import `casl_django.models.UserPermission` and create objects as desired.

Quick start
-----------

1. Add "casl_django" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'casl_django',
    ]

2. Run `python manage.py migrate` to create the models.


API
---

By default, your user object should contain a related relationship called `casl_permissions`.
You can filter by `permission__subject` and `permission__action` and finally get the rules with
the queryset method `bundle()`.

--------
bundle()
--------

This method it's included in the QuerySet's for `UserPermissions` (user.casl_permissions) and for
`CASLPermission` (CASLPermission.objects).

This method returns a list like the following::

    [
        // These are regular django permissions transformed to CASL-Style rules
        {'subject': 'products/item', actions: ['add', 'change']},
        // These are CASLPermissions objects
        {'subject': 'navigation', actions: ['index', 'products']}
    ]

The bundle consists in grouping same-subject rules and the actions, having less data
to send over the wire.