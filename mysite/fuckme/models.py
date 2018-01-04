# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=30)
    birth = models.DateTimeField()
    position = models.IntegerField(default=1)


class Good(models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    proday = models.DateTimeField()
    shelflife = models.IntegerField()
    gtype = models.IntegerField()



