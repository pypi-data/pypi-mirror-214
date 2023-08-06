"""
Copyright (c) 2014-present, aglean Inc.
"""
import operator
from functools import reduce

from ariadne_relay import from_global_id
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.models.query import QuerySet

from .models import Organization, Membership


async def resolve_anorganizations(obj, info, connection_args, **kwargs):
    name = kwargs.get('name', '')
    dn = kwargs.get('dn', '')

    queryset = []
    lookups = []

    if name:
        lookups.append(Q(name__icontains=name))

    if dn:
        lookups.append(Q(name_icontains=dn))

    if lookups:
        queryset = await sync_to_async(obj.filter)(reduce(operator.and_,
                                                          lookups)) \
                if isinstance(obj, QuerySet) \
                else await sync_to_async(Organization.objects.filter)(
                        reduce(operator.and_, lookups))
    else:
        queryset = obj if isinstance(obj, QuerySet) \
                else await sync_to_async(Organization.objects.all)()

    return queryset


async def resolve_users(obj, info, connection_args, **kwargs):
    username = kwargs.get('username', '')
    first_name = kwargs.get('first_name', '')
    last_name = kwargs.get('last_name', '')
    email = kwargs.get('email', '')
    is_active = kwargs.get('is_active', None)

    queryset = []
    lookups = []

    if username:
        lookups.append(Q(username__icontains=username))

    if first_name:
        lookups.append(Q(first_name__icontains=first_name))

    if last_name:
        lookups.append(Q(last_name__icontains=last_name))

    if email:
        lookups.append(Q(email__icontains=email))

    if is_active is not None:
        lookups.append(Q(is_active=is_active))

    if lookups:
        queryset = await sync_to_async(obj.filter)(reduce(operator.and_,
                                                          lookups)) \
                if isinstance(obj, QuerySet) \
                else await sync_to_async(get_user_model().objects.filter)(
                        reduce(operator.and_, lookups))
    else:
        queryset = obj if isinstance(obj, QuerySet) \
                else await sync_to_async(get_user_model().objects.all)()

    return queryset


async def resolve_anorganization_memberships(obj, indo, connection_args,
                                             **kwargs):
    user = kwargs.get('user', '')
    organization = kwargs.get('organization', '')
    serial_number = kwargs.get('serial_number', '')
    dn = kwargs.get('dn', '')
    is_valid = kwargs.get('is_valid', None)

    queryset = []
    lookups = []

    if user:
        _, id = from_global_id(user)
        lookups.append(Q(user=id))

    if organization:
        _, id = from_global_id(organization)
        lookups.append(Q(organization=id))

    if serial_number:
        lookups.append(Q(serial_number__icontains=serial_number))

    if dn:
        lookups.append(Q(name_icontains=dn))

    if is_valid is not None:
        lookups.append(Q(is_valid=is_valid))

    if lookups:
        queryset = await sync_to_async(obj.filter)(reduce(operator.and_,
                                                          lookups)) \
                if isinstance(obj, QuerySet) \
                else await sync_to_async(Membership.objects.filter)(
                        reduce(operator.and_, lookups))
    else:
        queryset = obj if isinstance(obj, QuerySet) \
                else await sync_to_async(Membership.objects.all)()

    return queryset
