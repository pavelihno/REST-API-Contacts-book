from django.db import models

import django.db.models


class PhoneNumber(models.Model):

    title = models.CharField(max_length=100, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)


class Contact(models.Model):

    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=200, null=True, blank=True)
    phone_numbers = models.ManyToManyField(to=PhoneNumber, related_name='contacts')

