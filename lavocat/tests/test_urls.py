from django.shortcuts import resolve_url as r
from django.test import Client

from lavocat.unittest_assertions import unittest_assert_redirects


def test_404_should_redirect():
    client = Client()
    response = client.get('/', follow=True)
    unittest_assert_redirects(response, r('api-v1:docs'))
