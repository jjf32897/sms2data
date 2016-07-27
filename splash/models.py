from __future__ import unicode_literals

from django.db import models

class Element(models.Model):
	datum = models.CharField(max_length=500) # the actual information, whether it's plaintext or a URL
	is_media = models.BooleanField(default=True) # is it media or is it just text?

# model to store bits of information for people
class Dataset(models.Model):
	number = models.CharField(max_length=15) # sender's number for rudimentary authentication
	identifier = models.CharField(max_length=20) # identification for this particular dataset
	elements = models.ManyToManyField(Element) # each dataset holds one or more elements
