from django.db import models


class Attendance(models.Model):
    customer_name = models.CharField(max_length=128)
    document_id = models.IntegerField()


class Attachment(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.DO_NOTHING)
    attachment = models.FileField(upload_to='documentos/')
