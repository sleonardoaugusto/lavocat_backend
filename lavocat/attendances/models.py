from django.db import models

from lavocat.attendances.validators import validate_document_id
from lavocat.core.models import ModelBase


class Attendance(ModelBase):
    customer_name = models.CharField(max_length=128)
    document_id = models.IntegerField(validators=[validate_document_id])


class AttendanceFile(ModelBase):
    attendance = models.ForeignKey(
        Attendance, on_delete=models.DO_NOTHING, related_name='files'
    )
    file = models.FileField(null=False, upload_to='documentos/')
