from django.db import models

from lavocat.core.models import ModelBase


class Attendance(ModelBase):
    customer_name = models.CharField(max_length=128)
    document_id = models.IntegerField()


class Attachment(ModelBase):
    attendance = models.ForeignKey(Attendance, on_delete=models.DO_NOTHING)
    attachment = models.FileField(upload_to='documentos/')
