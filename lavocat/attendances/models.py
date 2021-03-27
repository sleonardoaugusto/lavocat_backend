from django.db import models

from lavocat.attendances.validators import validate_document_id
from lavocat.core.models import ModelBase


class AttendanceStatus(models.IntegerChoices):
    PENDING_DOCS = 1, 'Documentação Pendente'
    PARTIAL_DOCS = 2, 'Documentação Parcial'
    TO_CONTACT = 3, 'À Contatar'
    DONE = 4, 'Concluído'


class Attendance(ModelBase):
    customer_name = models.CharField(max_length=128)
    document_id = models.IntegerField(validators=[validate_document_id])
    status = models.PositiveSmallIntegerField(choices=AttendanceStatus.choices)
    resume = models.TextField(null=True)


def upload_to(instance, fname):
    document_id = instance.attendance.document_id
    return f'documentos/{document_id}/{fname}'


class AttendanceFile(ModelBase):
    attendance = models.ForeignKey(
        Attendance, on_delete=models.DO_NOTHING, related_name='files'
    )
    file = models.FileField(null=False, upload_to=upload_to)
