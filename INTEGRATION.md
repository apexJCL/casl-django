# Implementation notes

The following it's just an opinion on how you can handle the implementation of CASL
paired with this package.

## Persistence on client-side

You can persist the rules serializing them to the `localStorage` (if you're using CASL on the browser),
or any other way, the rules returned by the server comply with the object notation CASL uses.

## Custom Rules

This package allows converting default django permissions to a CASL rule, but you can also create
your own custom rules.

Let's say you want to have control over the navigation on your SPA, so you have the following structure:

```

+ /
  + admin/
  + login/
  + profile/

```

In theory, you want the following user profiles:

```
Unauthorized user:

+ Can only see index and login

Authorized user:

+ Can see index and profile

Admin user:

+ Can see index, profile and admin section
```

You can declare the following routes:

```
{
    subject: 'navigate',
    actions: ['index', 'login', 'profile', 'admin', ]
}
```

Then, in your frontend you can check on your router:

```js

if (ability.can(route, 'navigate')) {
    // do something
}
redirect(404)

```

And for the default rules declaration, you can have the following: 
```js
AbilityBuilder.define(can => {
    can(['index', 'login'], 'navigate')
})
```

This way, your default user can only navigate to either `index` and `login`, then, after they
login, you can pull the new permissions and update the app according to it.

**TL;DR:** you can use the custom rules to enforce application-wide permissions, or anything
you're thinking to do.


## Managers and sources

There are plans to create packages that can provide access to CASL rules from different ways:

+ REST API
+ GraphQL
+ Websocket

This section will be updated according to the progress on the other implementations.
