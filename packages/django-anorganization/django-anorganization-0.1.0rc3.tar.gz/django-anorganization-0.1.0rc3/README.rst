====================================
django app of an organization
====================================

Anorganization uses membership, and organization models to group users.
Support for Ariadne graphQL with pre-defined types and basic resolvers.

------------
Requirements
------------

* Python 3.10+
* django 4.0+
* pillow 9.4.0+

--------
Settings
--------
Store uploaded file with tokenize file name, default to False

* ANORGANIZATION_USE_TOKEN_FILENAME = True

-------------------
Django admin mixins
-------------------

Use predefined mixins to construct the admin class.

* OrganizationAdminMixin
* MembershipAdminMixin

.. code:: python

    from django.contrib import admin

    from anorganization.models import Organization
    from anorganization.mixins import OrganizationAdminMixin


    @admin.register(Organization)
    class OrganizationAdmin(OrganizationAdminMixin, ModelAdmin):
        ...

---------------------------
Ariadne types and resolvers
---------------------------

Integrate predefined types and resolvers to scheme.

Requirements
------------

* ariadne 0.16.0+
* ariadne-relay 0.1.0a8+

**schema**

.. code:: python

   from anorganization.graphqls import anorganization_schema


* anarticle/graphqls/article.graphql
* anarticle/graphqls/tag.graphql

**types**

.. code:: python

   from anorganization.graphqls import anorganization_bindables


* anorganization
* anorganization_membership

**resolvers**

Async version

.. code:: python

   from anorganization.graphqls import resolve_anorganization_instance, \
           resolve_anorganization_member_connection, resolve_anorganizations

   anorganization.set_instance_resolver(resolve_anorganization_instance)
   anorganization.set_connection('members', resolve_anorganization_member_connection)

   query.set_field('organizations', resolve_anorganizations)


* resolve_anorganization_instance
* resolve_anorganization_member_connection
* resolve_anorganization_membership_instance
* resolve_anorganizations
* resolve_anorganization_memberships

Sync version

* resolve_anorganization_instance_sync
* resolve_anorganization_member_connection_sync
* resolve_anorganization_membership_instance_sync
* resolve_anorganizations_sync
* resolve_anorganization_memberships_sync

-------
License
-------

django-anarticle is released under the terms of **Apache license**. Full details in LICENSE file.
