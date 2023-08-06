"""
Copyright (c) 2014-present, aglean Inc.
"""
import operator
from functools import reduce

from ariadne import convert_kwargs_to_snake_case
from ariadne_relay import NodeObjectType, from_global_id
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.models.query import QuerySet

from .models import Organization, Membership


anorganization = NodeObjectType('AnOrganization')


@anorganization.instance_resolver
def resolve_anorganization_instance(id, *_):
    return Organization.objects.get(id=id)


@anorganization.connection('members')
def resolve_anorganization_member_connection(obj, info, **kwargs):
    return resolve_users(obj.members, info, kwargs)


@convert_kwargs_to_snake_case
def resolve_anorganizations(obj, info, **kwargs):
    name = kwargs.get('name', '')
    dn = kwargs.get('dn', '')

    queryset = []
    filters = []

    if name:
        filters.append(Q(name__icontains=name))

    if dn:
        filters.append(Q(name_icontains=dn))

    if filters:
        queryset = obj.filter(reduce(operator.and_, filters)) \
                if isinstance(obj, QuerySet) \
                else Organization.objects.filter(reduce(operator.and_,
                                                        filters))
    else:
        queryset = obj if isinstance(obj, QuerySet) \
                else Organization.objects.all()

    return queryset


@convert_kwargs_to_snake_case
def resolve_users(obj, info, **kwargs):
    username = kwargs.get('username', '')
    first_name = kwargs.get('first_name', '')
    last_name = kwargs.get('last_name', '')
    email = kwargs.get('email', '')
    is_active = kwargs.get('is_active', None)

    queryset = []
    filters = []

    if username:
        filters.append(Q(username__icontains=username))

    if first_name:
        filters.append(Q(first_name__icontains=first_name))

    if last_name:
        filters.append(Q(last_name__icontains=last_name))

    if email:
        filters.append(Q(email__icontains=email))

    if is_active is not None:
        filters.append(Q(is_active=is_active))

    if filters:
        queryset = obj.filter(reduce(operator.and_, filters)) \
                if isinstance(obj, QuerySet) \
                else get_user_model().objects.filter(reduce(operator.and_,
                                                            filters))
    else:
        queryset = obj if isinstance(obj, QuerySet) \
                else get_user_model().objects.all()

    return queryset


anorganization_membership = NodeObjectType('AnOrganizationMembership')


@anorganization_membership.instance_resolver
def resolve_anorganization_membership_instance(id, *_):
    return Membership.objects.get(id=id)


@convert_kwargs_to_snake_case
def resolve_anorganization_memberships(obj, indo, **kwargs):
    user = kwargs.get('user', '')
    organization = kwargs.get('organization', '')
    serial_number = kwargs.get('serial_number', '')
    dn = kwargs.get('dn', '')
    is_valid = kwargs.get('is_valid', None)

    queryset = []
    filters = []

    if user:
        _, id = from_global_id(user)
        filters.append(Q(user=id))

    if organization:
        _, id = from_global_id(organization)
        filters.append(Q(organization=id))

    if serial_number:
        filters.append(Q(serial_number__icontains=serial_number))

    if dn:
        filters.append(Q(name_icontains=dn))

    if is_valid is not None:
        filters.append(Q(is_valid=is_valid))

    if filters:
        queryset = obj.filter(reduce(operator.and_, filters)) \
                if isinstance(obj, QuerySet) \
                else Membership.objects.filter(reduce(operator.and_, filters))
    else:
        queryset = obj if isinstance(obj, QuerySet) \
                else Membership.objects.all()

    return queryset


types = [anorganization, anorganization_membership]
