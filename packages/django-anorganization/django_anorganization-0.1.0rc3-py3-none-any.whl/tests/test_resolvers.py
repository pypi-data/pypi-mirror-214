"""
Copyright (c) 2014-present, aglean Inc.
"""
import pytest
from django.contrib.auth import get_user_model

from anorganization.models import Organization, Membership
from anorganization.resolvers import resolve_anorganizations, \
        resolve_anorganization_memberships


@pytest.fixture(scope='module')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user_1 = get_user_model().objects.create_user('John')
        user_2 = get_user_model().objects.create_user('Marry')

        org_1 = Organization.objects.create(name='red')
        org_2 = Organization.objects.create(name='black')
        org_3 = Organization.objects.create(name='white')

        member_1 = Membership.objects.create(user=user_1,
                                             organization=org_1)
        member_2 = Membership.objects.create(user=user_1,
                                             organization=org_1)
        member_3 = Membership.objects.create(user=user_2,
                                             organization=org_2,
                                             is_valid=False)


class TestOrganization:
    @pytest.mark.django_db
    def test_resolve_organizations_from_root_without_args(self):
        assert resolve_anorganizations(None, None).count() == 3

    @pytest.mark.django_db
    def test_resolve_organizations_from_root_with_args(self):
        assert resolve_anorganizations(None, None, name='ack').count() == 1

    @pytest.mark.django_db
    def test_resolve_organizations_from_obj_without_args(self):
        queryset = Organization.objects.all()
        assert resolve_anorganizations(queryset, None).count() == 3

    @pytest.mark.django_db
    def test_resolve_organizations_from_obj_with_args(self):
        queryset = Organization.objects.all()
        assert resolve_anorganizations(queryset, None, name='ack').count() == 1


class TestMembership:
    @pytest.mark.django_db
    def test_resolve_memberships_from_root_without_args(self):
        assert resolve_anorganization_memberships(None, None).count() == 3

    @pytest.mark.django_db
    def test_resolve_memberships_from_root_with_args(self):
        assert resolve_anorganization_memberships(None, None,
                                                  is_valid=False).count() == 1

    @pytest.mark.django_db
    def test_resolve_memberships_from_obj_without_args(self):
        queryset = Membership.objects.all()
        assert resolve_anorganizations(queryset, None).count() == 3

    @pytest.mark.django_db
    def test_resolve_memberships_from_obj_with_args(self):
        queryset = Membership.objects.all()
        assert resolve_anorganization_memberships(queryset,
                                                  None,
                                                  is_valid=False).count() == 1
