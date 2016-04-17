from django.db import models
from geopy.geocoders import GoogleV3
from django.conf import settings

FOR_SALE = 'F'
SOLD = 'S'
LISTING_OPTIONS = ((FOR_SALE, 'For Sale'), (SOLD, 'Sold'))

METRIC = 'M'
IMPERIAL = 'I'
UNITS_OPTIONS = ((METRIC, 'metric'), (IMPERIAL, 'imperial'))

FLAG_EXACT = 'E'
FLAG_SIMILAR = 'S'
FLAG_OPTIONS = ((FLAG_EXACT, 'exact duplicate'), (FLAG_SIMILAR, 'merge candidate'))

class Property(models.Model):
    """ A Property object representing a snapshot of a property at a point in
    time.

    A given physical residence may be represented multiple times if one of its
    properties changes. For example if a property is sold a second time at a new
    price.

    A property also contains a number of :class:`.Feature` objects which allow
    the presence of optional things like a pool or a skylight which would
    otherwise crowd the number of fields in the mdoel.
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

    # Blank and Null for backwards compatibility
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    # So we can keep ones that get flagged as a reference
    valid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Save the model after geocoding the supplied address.

        Here the address is geocoded using the Google geocoding service.
        This is limited to 2500 requests per day. There is no current system
        to account for this so models over 2500 will not geocode.
        """
        if self.valid:
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


class Flag(models.Model):
    """ A flagged duplication of two properties which are similar.

    These flags are then resolved by a user with resolution rights. This
    may be a human or a bot.
    """
    first_object = models.ForeignKey(Property, blank=True, 
                                     null=True, related_name="first")
    second_object = models.ForeignKey(Property, blank=True, 
                                      null=True, related_name="second")
    flag_type = models.CharField(max_length=1, choices=FLAG_OPTIONS)
    is_open = models.BooleanField(default=True)
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_submitted = models.DateTimeField(auto_now=True)

    def is_valid(self):
        """If a flag is still open it needs to point to two objects.
        
        Once it has been closed one or both of those objects may have
        been removed.
        """
        if self.is_open:
            return (self.first_object is not None) and (self.second_object is not None)
        return True


class Resolution(models.Model):
    """ Documented resolutions to duplications in data.
    """
    flag = models.ForeignKey(Flag)
    resolver = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_resolved = models.DateTimeField(auto_now=True)
    note = models.CharField(max_length=512, blank=True, null=True)
    final_object = models.ForeignKey(Property)

