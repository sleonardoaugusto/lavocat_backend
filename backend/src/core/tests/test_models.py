import pytest
from model_bakery import baker

from src.core.models import UserAllowed


@pytest.fixture
def record():
    return baker.make('UserAllowed')


def test_should_exist(record):
    assert UserAllowed.objects.all().exists()
