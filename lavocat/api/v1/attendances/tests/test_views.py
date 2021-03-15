from django.test import TestCase
from model_bakery import baker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from lavocat.api.v1.attendances.serializers import AttendanceSerializer
from lavocat.attendances.models import Attendance


class Client:
    client = APIClient()


class AttendanceViewsetGetTest(TestCase, Client):
    def setUp(self) -> None:
        self.resp = self.client.get(reverse('api-v1:attendance-list'))

    def test_get(self):
        self.assertEqual(self.resp.status_code, status.HTTP_200_OK)


class AttendanceViewsetPostTest(TestCase, Client):
    def setUp(self) -> None:
        data = baker.prepare('Attendance')
        payload = AttendanceSerializer(data).data
        self.resp = self.client.post(
            reverse('api-v1:attendance-list'), payload, content_type='application/json'
        )

    def test_post(self):
        self.assertEqual(self.resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attendance.objects.all().count(), 1)
