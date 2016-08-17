import django_filters
import math
from api.models import Property, Feature
from rest_framework import filters
from ast import literal_eval as make_tuple
from django.db.models import F

class PropertyFilter(filters.FilterSet):
    """Filters used for the Property model.

    Filters are added to a request as query parameters. For example the follwoing
    request will filter based on the minimum hosue price.

    `/api/property?min_price=100000`

    while not an explicit attribute of this class the `features` property can
    also be filtered on by suppluing a list of the feature ids. For example:

    `/api/property?features=1`
    

    Attributes:
        min_price: Supplying this filter returns only properties with a price
            greater than or equal to the supplied value.

        max_price: Supplying this filter returns only properties with a price
            less than or equal to the supplied value.
        
        min_bedrooms: Supplying this filter returns only properties which have
            a number of bedrooms greater than or equal to the supplied value.
        
        max_bedrooms: Supplying this filter returns only properties which have
            a number of bedrooms less than or equal to the supplied value.
        
        min_bathrooms: Supplying this filter returns only properties which have
            a number of bathrooms greater than or equal to the supplied value.
        
        max_bathrooms: Supplying this filter returns only properties which have
            a number of bathrooms less than or equal to the supplied value.
        
        min_car_spaces: Supplying this filter returns only properties which have
            a number of car spaces greater than or equal to the supplied value.
        
        max_car_spaces: Supplying this filter returns only properties which have
            a number of car_spaces less than or equal to the supplied value.
        
        address_contains: Supplying this filter will return only properties which
            contain the supplied text in their geocded address.
        
    """

    min_price = django_filters.NumberFilter(name="price", lookup_type="gte")
    max_price = django_filters.NumberFilter(name="price", lookup_type="lte")

    min_bedrooms = django_filters.NumberFilter(name="bedrooms", lookup_type="gte")
    max_bedrooms = django_filters.NumberFilter(name="bedrooms", lookup_type="lte")

    min_bathrooms = django_filters.NumberFilter(name="bathrooms", lookup_type="gte")
    max_bathrooms = django_filters.NumberFilter(name="bathrooms", lookup_type="lte")

    min_car_spaces = django_filters.NumberFilter(name="car_spaces", lookup_type="gte")
    max_car_spaces = django_filters.NumberFilter(name="car_spaces", lookup_type="lte")

    close_to = django_filters.MethodFilter(action='filter_approx_distance')

    class Meta:
        model = Property
        fields = ["min_price", "max_price", "min_bedrooms", "max_bedrooms", 
                "min_bathrooms", "max_bathrooms", "min_car_spaces", "max_car_spaces",
                "features", "close_to"]


    def filter_approx_distance(self, queryset, value):
        """ Filters all results who's address object has a lat long approximatly value[0] from value[1]
        """
        # Assume value is in the form (distance, lat, long)
        try:
            vals = make_tuple(value)
        except:
            # if something bad happened just fallabck to not working for now
            return queryset

        # remove queryset objects tha have no address
        queryset = queryset.filter(address_object__isnull=False)

        pi = 3.1415
        f_lat = pi*(vals[1] - F('address_object__latitude'))/180.0
        f_long = pi*(vals[2] - F('address_object__longitude'))/180.0
        m_lat = 0.5*pi*(vals[1] + F('address_object__latitude'))/180.0
        cosprox = 1 - (m_lat**2)/2.0 # approximate cosine
        
        approx_dist = (6371**2)*(f_lat**2 + (cosprox*f_long)**2)

        queryset = queryset.annotate(dist=(approx_dist - vals[0]**2)).annotate(flat=f_lat)
        queryset = queryset.filter(dist__lte=0)

        return queryset
