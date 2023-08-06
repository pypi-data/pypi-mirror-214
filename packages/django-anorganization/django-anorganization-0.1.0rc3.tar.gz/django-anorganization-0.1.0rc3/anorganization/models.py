"""
Copyright (c) 2014-present, aglean Inc.
"""
from django.conf import settings
from django.db import models

from .utils import image_path, image_url


class Organization(models.Model):
    # relationship
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     through='Membership')

    # detail
    name = models.CharField(max_length=255)
    dn = models.CharField(max_length=255, blank=True)
    attributes = models.JSONField(blank=True)
    image = models.ImageField(
        upload_to=image_path,
        help_text=(
            'Upload file should under size limitation, '
            'with png, jpg or jpeg file extensions.'
        ),
        blank=True
    )

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        return image_url(self)

    @property
    def valid_member_count(self):
        return self.members.filter(membership__is_valid=True).count()

    @property
    def invalid_member_count(self):
        return self.members.filter(membership__is_valid=False).count()


class Membership(models.Model):
    # relationship
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    # detail
    serial_number = models.CharField(max_length=100, blank=True)
    dn = models.CharField(max_length=255, blank=True)
    attributes = models.JSONField(blank=True)
    image = models.ImageField(
        upload_to=image_path,
        help_text=(
            'Upload file should under size limitation, '
            'with png, jpg or jpeg file extensions.'
        ),
        blank=True
    )

    # flag
    is_valid = models.BooleanField(
        help_text='Designates whether the membership is valid.',
        default=True
    )

    # datetime
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.user.username

    @property
    def image_url(self):
        return image_url(self)
