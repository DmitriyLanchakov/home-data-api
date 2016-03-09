from django.db import models


class SimpleProperty(models.Model):
    """ A (very) simple property model

    Not named Property to make it easier to drop and replace with a real model.
    """
    address = models.CharField(max_length=512)
    
    bedrooms = models.FloatField()
    bathrooms = models.FloatField()

    price = models.FloatField()
