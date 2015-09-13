# -*- coding: utf-8 -*-
from django.db import models


class Bio(models.Model):
    first_name = models.CharField('Name', max_length=50)
    last_name = models.CharField('Last name', max_length=50)
    date_of_birth = models.DateField('Date of birth')
    bio = models.TextField('Bio', blank=True)
    email = models.EmailField('Email')
    jabber = models.CharField('Jabber', max_length=255, blank=True)
    skype = models.CharField('Skype', max_length=255, blank=True)
    other_contacts = models.TextField('Other contacts', blank=True)

    class Meta:
        verbose_name = 'Bio'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return u'{0} - {1}'.format(self.first_name, self.last_name)
