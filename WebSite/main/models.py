from __future__ import unicode_literals

from django.db import models

class cropLabel(models.Model):
    srcFile = models.CharField( max_length=200 )
    x = models.IntegerField( default=0 )
    y = models.IntegerField( default=0 )
    width = models.IntegerField( default=0 )
    height = models.IntegerField( default=0 )
    duration = models.BigIntegerField( default=0 )
    
class cropField(models.Model):
    srcFile = models.CharField( max_length=200 )
    field = models.SmallIntegerField( default=5 )
    x = models.IntegerField( default=0 )
    y = models.IntegerField( default=0 )
    width = models.IntegerField( default=0 )
    height = models.IntegerField( default=0 )
    duration = models.BigIntegerField( default=0 )    
    
