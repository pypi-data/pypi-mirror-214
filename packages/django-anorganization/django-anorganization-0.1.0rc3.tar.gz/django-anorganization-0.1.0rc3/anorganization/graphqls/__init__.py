"""
Copyright (c) 2014-present, aglean Inc.
"""
from ariadne import load_schema_from_path

from .type_defs import (
    anorganization,
    anorganization_membership,
    resolve_anorganization_instance,
    resolve_anorganization_member_connection,
    resolve_anorganization_membership_instance,
    resolve_anorganization_instance_sync,
    resolve_anorganization_member_connection_sync,
    resolve_anorganization_membership_instance_sync
)
from .bindables import (
    resolve_anorganizations,
    resolve_anorganization_memberships
)
from .bindables_sync import (
    resolve_anorganizations_sync,
    resolve_anorganization_memberships_sync
)


anorganization_schema = load_schema_from_path('anorganization/graphqls')

anorganization_bindables = [anorganization, anorganization_membership]


__all__ = [
    'anorganization_schema',
    'anorganization_bindables',
    resolve_anorganization_instance,
    resolve_anorganization_member_connection,
    resolve_anorganization_membership_instance,
    resolve_anorganization_instance_sync,
    resolve_anorganization_member_connection_sync,
    resolve_anorganization_membership_instance_sync,
    resolve_anorganizations,
    resolve_anorganization_memberships,
    resolve_anorganizations_sync,
    resolve_anorganization_memberships_sync
]
