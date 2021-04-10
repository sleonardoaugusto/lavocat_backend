import pytest
from model_bakery import baker

from lavocat.core.models import UserAllowed


@pytest.fixture
def record():
    return baker.make('UserAllowed')


def test_must_exist(record):
    assert UserAllowed.objects.all().exists()
