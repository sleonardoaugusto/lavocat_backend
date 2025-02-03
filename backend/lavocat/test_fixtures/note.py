import pytest
from model_bakery import baker

from lavocat.attendances.models import Note, ServicesTypesOptions


@pytest.fixture
def note(attendance) -> Note:
    return baker.make(
        "Note",
        attendance=attendance,
        deleted_at=None,
        _fill_optional=True,
    )


@pytest.fixture
def note_dpvat(attendance) -> Note:
    if attendance.services_types:
        attendance.services_types.append(ServicesTypesOptions.DPVAT)
    else:
        attendance.services_types = [ServicesTypesOptions.DPVAT]
    attendance.save()
    return baker.make(
        "Note",
        attendance=attendance,
        header=ServicesTypesOptions.DPVAT.label,
        deleted_at=None,
        _fill_optional=True,
    )


@pytest.fixture
def note_auxilio_doenca(attendance) -> Note:
    if attendance.services_types:
        attendance.services_types.append(ServicesTypesOptions.AUXILIO_DOENCA)
    else:
        attendance.services_types = [ServicesTypesOptions.AUXILIO_DOENCA]
    attendance.save()
    return baker.make(
        "Note",
        attendance=attendance,
        header=ServicesTypesOptions.AUXILIO_DOENCA.label,
        deleted_at=None,
        _fill_optional=True,
    )
