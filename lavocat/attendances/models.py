from django.db import models

from lavocat.attendances.validators import validate_document_id
from lavocat.core.models import ModelBase
from storage_backends import MediaStorage


class AttendanceStatus(models.IntegerChoices):
    PENDING_DOCS = 1, 'Documentação pendente'
    PARTIAL_DOCS = 2, 'Em andamento'
    TO_CONTACT = 3, 'À contatar'
    DONE = 4, 'Concluído'


class Attendance(ModelBase):
    customer_name = models.CharField(max_length=128)
    document_id = models.CharField(
        null=True, blank=True, max_length=11, validators=[validate_document_id]
    )
    status = models.PositiveSmallIntegerField(choices=AttendanceStatus.choices)
    resume = models.TextField(null=True)
    status_resume = models.TextField(null=True)

    class Meta:
        ordering = ['-updated_at']


def upload_to(instance, fname):
    attendance_pk = instance.attendance.pk
    return f'documentos/{attendance_pk}/{fname}'


class AttendanceFile(ModelBase):
    attendance = models.ForeignKey(
        Attendance, on_delete=models.CASCADE, related_name='files'
    )
    file = models.FileField(null=False, upload_to=upload_to, storage=MediaStorage())

    # TODO tests
    def delete(self, using=None, keep_parents=False):
        self.file.storage.delete(self.file.name)
        super().delete()
