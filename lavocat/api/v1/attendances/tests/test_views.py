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

    def test_url(self):
        self.assertEqual(self.resp.status_code, status.HTTP_200_OK)


class AttendanceViewsetPostTest(TestCase, Client):
    def setUp(self) -> None:
        data = dict(customer_name='Valeu Natalina', document_id=99999999999)
        attendance = baker.prepare('Attendance', **data)
        self.serializer = AttendanceSerializer
        payload = self.serializer(attendance).data
        self.resp = self.client.post(
            reverse('api-v1:attendance-list'),
            payload,
            content_type='application/json',
        )

    def test_must_exist(self):
        self.assertEqual(Attendance.objects.all().count(), 1)

    def test_status_returned(self):
        self.assertEqual(self.resp.status_code, status.HTTP_201_CREATED)

    def test_content_returned(self):
        expect = self.serializer(Attendance.objects.all().first()).data
        self.assertDictEqual(self.resp.json(), expect)


class AttendanceFileViewsetGetTest(TestCase, Client):
    def setUp(self) -> None:
        self.resp = self.client.get(reverse('api-v1:attendancefile-list'))

    def test_url(self):
        self.assertEqual(self.resp.status_code, status.HTTP_200_OK)
