from django.db import models
from geopy.geocoders import GoogleV3

FOR_SALE = 'F'
SOLD = 'S'
LISTING_OPTIONS = ((FOR_SALE, 'For Sale'), (SOLD, 'Sold'))

METRIC = 'M'
IMPERIAL = 'I'
UNITS_OPTIONS = ((METRIC, 'metric'), (IMPERIAL, 'imperial'))


class Property(models.Model):
    """ A Property object representing a snapshot of a property at a point in
    time.

    A given physical residence may be represented multiple times if one of its
    properties changes. For example if a property is sold a second time at a new
    price.
    """
    upload_timestamp = models.DateTimeField(auto_now=True)
    
    listing_timestamp = models.DateTimeField()
    listing_type = models.CharField(max_length=1, choices=LISTING_OPTIONS)

    price = models.FloatField()

    bedrooms = models.FloatField(blank=True, null=True)
    bathrooms = models.FloatField(blank=True, null=True)
    car_spaces = models.FloatField(blank=True, null=True)

    building_size = models.FloatField(blank=True, null=True)
    land_size = models.FloatField(blank=True, null=True)
    size_units = models.CharField(max_length=1, choices=UNITS_OPTIONS)

    raw_address = models.CharField(max_length=512)
    geocoded_address = models.CharField(max_length=512)

    features = models.ManyToManyField('Feature', blank=True)

    def save(self, *args, **kwargs):
        encoder = GoogleV3()
        location = encoder.geocode(self.raw_address)
        self.geocoded_address = location.address
        super(Property, self).save(*args, **kwargs)


class Feature(models.Model):
    """ A boolean feature of a Property
    
    For things which a property may or may not have (eg a garden).
    """
    category = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)

    def __str__(self):
        return str(self.category) + ":" + str(self.tag)

class SimpleProperty(models.Model):
    """ A (very) simple property model

    Not named Property to make it easier to drop and replace with a real model.
    """
    address = models.CharField(max_length=512)
    
    bedrooms = models.FloatField()
    bathrooms = models.FloatField()

    price = models.FloatField()
