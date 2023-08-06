"""
Copyright (c) 2014-present, aglean Inc.
"""
from ariadne_relay import NodeObjectType

from .models import Organization, Membership
from .bindables import resolve_anorganization_memberships
from .bindables_sync import resolve_anorganization_memberships_sync


anorganization = NodeObjectType('AnOrganization')
anorganization_membership = NodeObjectType('AnOrganizationMembership')


async def resolve_anorganization_instance(id, *_):
    return await Organization.objects.aget(id=id)


async def resolve_anorganization_member_connection(obj, info, connection_args,
                                                   **kwargs):
    """resolve org connection to members"""
    return await resolve_anorganization_memberships(obj.members,
                                                    info,
                                                    connection_args,
                                                    kwargs)


async def resolve_anorganization_membership_instance(id, *_):
    return await Membership.objects.aget(id=id)


def resolve_anorganization_instance_sync(id, *_):
    return Organization.objects.get(id=id)


def resolve_anorganization_member_connection_sync(obj, info, connection_args,
                                                  **kwargs):
    """resolve org connection to members"""
    return resolve_anorganization_memberships_sync(obj.members, info,
                                                   connection_args, kwargs)


def resolve_anorganization_membership_instance_sync(id, *_):
    return Membership.objects.get(id=id)
