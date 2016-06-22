from django.db import models
from geopy.geocoders import GoogleV3
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from api.util import send_signup_email
import datetime
import random
import string
import requests

FOR_SALE = 'F'
SOLD = 'S'
APPRAISED = 'A'
LISTING_OPTIONS = ((FOR_SALE, 'For Sale'), (SOLD, 'Sold'), (APPRAISED, 'Appraised'))

METRIC = 'M'
IMPERIAL = 'I'
UNITS_OPTIONS = ((METRIC, 'metric'), (IMPERIAL, 'imperial'))

FLAG_EXACT = 'E'
FLAG_SIMILAR = 'S'
FLAG_OPTIONS = ((FLAG_EXACT, 'exact duplicate'), (FLAG_SIMILAR, 'merge candidate'))

class Profile(models.Model):
    """ Profile object to store extended data about the user.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, 
            on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)

    confirmation_code = models.CharField(max_length=512)
    confirmation_date = models.DateTimeField(auto_now=True)

    def update_code(self):
        """Generate a new email confirmation code.
        """
        self.confirmation_code = ''.join([random.choice(string.ascii_uppercase) 
                                          for _ in range(254)])
        self.confirmation_date = timezone.now()
        self.save()

    def get_confirmation_link(self):
        """Generate a url for confirming the account.

        This generates the relative uri and should be appended to the hostname.
        """
        return "/confirm/" + str(self.pk) + "/" + self.confirmation_code + "/"

    def can_confirm(self):
        """Can the user be confirmed?

        return true if the user is unconfirmed and the code is still valid
        """
        return (not self.confirmed) and (timezone.now() < self.confirmation_date + datetime.timedelta(days=2))


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, **kwargs):
    new_account = False
    if kwargs['created']:
        profile = Profile.objects.create(user=instance)
        new_account = True
    else:
        profile = Profile.objects.filter(user=instance)
        if len(profile) == 0:
            profile = Profile.objects.create(user=instance)
            new_account = True

    if new_account:
        profile.update_code()
        link_text = settings.HOSTNAME + profile.get_confirmation_link()
        if not settings.TESTING:
            send_signup_email(instance.email, link_text)


class Address(models.Model):
    raw = models.TextField()
    subpremise = models.IntegerField(null=True, blank=True)
    street_number = models.IntegerField()
    route = models.CharField(max_length=512)
    locality = models.CharField(max_length=512)
    area_level_2 = models.CharField(max_length=512)
    area_level_1 = models.CharField(max_length=512)
    country = models.CharField(max_length=128)
    postal_code = models.CharField(max_length=50)
    formatted_address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()


    def from_google_json(self, json):
        json = json['results'][0]
        for part in json['address_components']:
            if 'subpremise' in part['types']:
                self.subpremise = part['long_name']
                continue
            if 'street_number' in part['types']:
                self.street_number = part['long_name']
                continue
            if 'route' in part['types']:
                self.route = part['long_name']
                continue
            if 'locality' in part['types']:
                self.locality = part['long_name']
                continue
            if 'administrative_area_level_2' in part['types']:
                self.area_level_2 = part['long_name']
                continue
            if 'administrative_area_level_1' in part['types']:
                self.area_level_1 = part['long_name']
                continue
            if 'country' in part['types']:
                self.country = part['long_name']
                continue
            if 'postal_code' in part['types']:
                self.postal_code = part['long_name']
                continue

        self.formatted_address = json['formatted_address']

        self.latitude = json['geometry']['location']['lat']
        self.longitude = json['geometry']['location']['lng']


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
    address_object = models.ForeignKey(Address, blank=True, null=True)

    features = models.ManyToManyField('Feature', blank=True)

    # Blank and Null for backwards compatibility
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    # So we can keep ones that get flagged as a reference
    valid = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        """Save the model after geocoding the supplied address.

        Here the address is geocoded using the Google geocoding service.
        This is limited to 2500 requests per day. There is no current system
        to account for this so models over 2500 will not geocode.
        """
        if not settings.TESTING:
            response = requests.get(
                    'https://maps.googleapis.com/maps/api/geocode/json',
                    params={'address': self.raw_address,
                            'key': settings.G_APPS_KEY})
            if response.status_code == 200:
                address = Address()
                address.raw = response.text
                address.from_google_json(response.json())
                address.save()
                self.address_object = address
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

