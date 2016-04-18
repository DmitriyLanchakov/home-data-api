from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils import timezone



class AnonTests(APITestCase):
    """Tests the various endpoints as an anonymous user.
    """

    fixtures = ['groups.json']

    def setUp(self):
        # Create a sample property to check reading permissions
        user = get_user_model().objects.create_user(
                username="test",
                password="test",
                email="test@test.com")

        prop = Property.objects.create(
                listing_timestamp=timezone.now(),
                listing_type=FOR_SALE,
                price=1000,
                size_units=METRIC,
                raw_address="123 Fake St")

        Feature.objects.create(
                category="Test",
                tag="Test")

        flag = Flag.objects.create(
                flag_type=FLAG_EXACT,
                submitter=user)

        Resolution.objects.create(
                flag=flag,
                resolver=user,
                final_object=prop)
        
    def test_read_property(self):
        """Anonymous users should be able to see properties.
        """
        url = reverse('property-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_write_property(self):
        """Anonymous users should not be able to POST new properties.
        """
        url = reverse('property-list')
        data = {
                'listing_type': FOR_SALE,
                'price': 1234,
                'raw_address': '125 Fake St',
                }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Property.objects.count(), 1)

    def test_edit_property(self):
        """Anonymous users should not be able to PUT new properties.
        """
        url = reverse('property-detail', kwargs={'pk':1})
        data = {
                'listing_type': FOR_SALE,
                'price': 1234,
                'raw_address': '125 Fake St',
                'size_units': METRIC
                }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Property.objects.filter(price=1000).count(), 1)
        self.assertEqual(Property.objects.filter(price=1234).count(), 0)

    def test_delete_property(self):
        """Anonymous users should not be able to DELETE existing properties.
        """
        url = reverse('property-detail', kwargs={'pk':1})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Property.objects.count(), 1)

    def test_read_feature(self):
        """Anonymous users should be able to GET current features.
        """
        url = reverse('feature-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_write_feature(self):
        """Anonymous users should not be able to POST new features.
        """
        pass

    def test_edit_feature(self):
        """Anonymous users should not be able to PUT new features.
        """
        pass

    def test_delete_feature(self):
        """Anonymous users should not be able to DELETE exising features.
        """
        pass

    def test_read_flag(self):
        """Anonymous users should be able to GET current flags.
        """
        url = reverse('flag-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_write_flag(self):
        """Anonymous users should not be able to POST new flags.
        """
        pass

    def test_edit_flag(self):
        """Anonymous users should not be able to PUT new flags.
        """
        pass

    def test_delete_flag(self):
        """Anonymous users should not be able to DELETE exising flags.
        """
        pass
    
    def test_read_resolution(self):
        """Anonymous users should be able to GET current resolutions.
        """
        url = reverse('resolution-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_write_resolution(self):
        """Anonymous users should not be able to POST new resolutions.
        """
        pass

    def test_edit_resolution(self):
        """Anonymous users should not be able to PUT new resolutions.
        """
        pass

    def test_delete_resolution(self):
        """Anonymous users should not be able to DELETE exising resolutions.
        """
        pass


class PushGroupTests(APITestCase):
    """Tests the various endpoints as an user in the push group.
    """

    fixtures = ['groups.json']

    def setUp(self):
        # Create a sample property to check reading permissions
        user = get_user_model().objects.create_user(
                username="test",
                password="test",
                email="test@test.com")

        push_group = Group.objects.get(name="pushing")
        user.groups.add(push_group)
        user.save()

        # Bust the permissions cache
        user = get_user_model().objects.get(pk=user.pk)

        prop = Property.objects.create(
                listing_timestamp=timezone.now(),
                listing_type=FOR_SALE,
                price=1000,
                size_units=METRIC,
                raw_address="123 Fake St")

        Feature.objects.create(
                category="Test",
                tag="Test")

        flag = Flag.objects.create(
                flag_type=FLAG_EXACT,
                submitter=user)

        Resolution.objects.create(
                flag=flag,
                resolver=user,
                final_object=prop)

        self.client.force_authenticate(user=user)
        
    def test_read_property(self):
        """Push Group users should be able to see properties.
        """
        url = reverse('property-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_write_property(self):
        """Push Group users should be able to POST new properties.
        """
        url = reverse('property-list')
        data = {
                'listing_type': FOR_SALE,
                'price': 1234,
                'raw_address': '125 Fake St',
                'size_units': METRIC,
                'listing_timestamp': timezone.now()
                }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Property.objects.count(), 2)

    def test_edit_property(self):
        """Push Group users should not be able to PUT new properties.
        """
        url = reverse('property-detail', kwargs={'pk':1})
        data = {
                'listing_type': FOR_SALE,
                'price': 1235,
                'raw_address': '125 Fake St',
                'size_units': METRIC,
                'listing_timestamp': timezone.now()
                }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Property.objects.filter(price=1000).count(), 1)
        self.assertEqual(Property.objects.filter(price=1235).count(), 0)

    def test_delete_property(self):
        """Push Group users should not be able to DELETE existing properties.
        """
        url = reverse('property-detail', kwargs={'pk':1})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Property.objects.count(), 1)

    def test_read_feature(self):
        """Push Group users should be able to GET current features.
        """
        url = reverse('feature-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_write_feature(self):
        """Push Group users should not be able to POST new features.
        """
        pass

    def test_edit_feature(self):
        """Push Group users should not be able to PUT new features.
        """
        pass

    def test_delete_feature(self):
        """Push Group users should not be able to DELETE exising features.
        """
        pass

    def test_read_flag(self):
        """Push Group users should be able to GET current flags.
        """
        url = reverse('flag-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_write_flag(self):
        """Push Group users should not be able to POST new flags.
        """
        pass

    def test_edit_flag(self):
        """Push Group users should not be able to PUT new flags.
        """
        pass

    def test_delete_flag(self):
        """Push Group users should not be able to DELETE exising flags.
        """
        pass
    
    def test_read_resolution(self):
        """Push Group users should be able to GET current resolutions.
        """
        url = reverse('resolution-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_write_resolution(self):
        """Push Group users should not be able to POST new resolutions.
        """
        pass

    def test_edit_resolution(self):
        """Push Group users should not be able to PUT new resolutions.
        """
        pass

    def test_delete_resolution(self):
        """Push Group users should not be able to DELETE exising resolutions.
        """
        pass
