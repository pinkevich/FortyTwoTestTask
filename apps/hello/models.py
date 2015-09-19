# -*- coding: utf-8 -*-
from django.db import models

from PIL import Image

from fortytwo_test_task.settings import WIDTH_PHOTO_RESIZE, HEIGHT_PHOTO_RESIZE


class Bio(models.Model):
    first_name = models.CharField('Name', max_length=50)
    last_name = models.CharField('Last name', max_length=50)
    date_of_birth = models.DateField('Date of birth')
    bio = models.TextField('Bio', blank=True)
    email = models.EmailField('Email')
    jabber = models.CharField('Jabber', max_length=255, blank=True)
    skype = models.CharField('Skype', max_length=255, blank=True)
    other_contacts = models.TextField('Other contacts', blank=True)
    photo = models.ImageField('Photo', upload_to='photos',
                              blank=True, null=True)

    class Meta:
        verbose_name = 'Bio'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return u'{0} - {1}'.format(self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        super(Bio, self).save(*args, **kwargs)
        if self.photo:
            if self.photo.width > WIDTH_PHOTO_RESIZE \
                    or self.photo.height > HEIGHT_PHOTO_RESIZE:
                self.photo_resize()

    def photo_resize(self):
        img = Image.open(self.photo.path)
        img.thumbnail((WIDTH_PHOTO_RESIZE, HEIGHT_PHOTO_RESIZE),
                      Image.ANTIALIAS)
        img.save(self.photo.path)


class HttpRequest(models.Model):
    ip = models.CharField('Remote address', max_length=255)
    page = models.URLField('View page')
    time = models.DateTimeField('Time', auto_now_add=True)
    header = models.TextField('Header')
    is_read = models.BooleanField('Is read', default=False)

    class Meta:
        verbose_name = 'Request'
        verbose_name_plural = 'Requests'

    def __unicode__(self):
        return u'{0} - {1}'.format(self.ip, self.page)
