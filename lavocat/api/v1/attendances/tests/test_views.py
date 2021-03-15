from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


class Client:
    client = APIClient()


class AttendanceViewsetTest(TestCase, Client):
    def test_get(self):
        resp = self.client.get(reverse('api-v1:attendance-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
