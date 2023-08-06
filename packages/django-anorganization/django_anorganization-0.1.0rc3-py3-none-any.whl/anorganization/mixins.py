"""
Copyright (c) 2014-present, aglean Inc.
"""


class OrganizationAdminMixin():
    ordering = ('name',)
    list_display = ('id', 'name', 'dn', 'image', 'image_url',
                    'valid_member_count', 'invalid_member_count')
    search_fields = ('name',)


class MembershipAdminMixin():
    ordering = ('-updated_at',)
    list_display = ('id', 'user', 'organization', 'serial_number', 'dn',
                    'is_valid', 'created_at', 'updated_at')
    list_filter = ('organization__name', 'is_valid')
    search_fields = ('user__username', 'organization__name')
    autocomplete_fields = ('user', 'organization')
