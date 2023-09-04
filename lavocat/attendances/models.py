from django.db import models
from multiselectfield import MultiSelectField

from lavocat.attendances.validators import validate_document_id
from lavocat.core.models import ModelBase
from storage_backends import MediaStorage

import uuid


class AttendanceStatus(models.IntegerChoices):
    PENDING_DOCS = 1, 'Documentação pendente'
    PARTIAL_DOCS = 2, 'Em andamento'
    TO_CONTACT = 3, 'À contatar'
    DONE = 4, 'Concluído'


class ServicesOffered(models.TextChoices):
    DPVAT = 'DPVAT', 'DPVAT'
    AUXILIO_DOENCA = 'AUXILIO_DOENCA', 'Auxílio Doença'
    AUXILIO_ACIDENTE = 'AUXILIO_ACIDENTE', 'Auxílio Acidente'
    LOAS = 'LOAS', 'LOAS'
    APOSENTADORIA = 'APOSENTADORIA', 'Aposentadoria'
    ACAO_CONTRA_CONDUTOR = 'ACAO_CONTRA_CONDUTOR', 'Ação Contra Condutor'
    ACAO_TRABALHISTA = 'ACAO_TRABALHISTA', 'Ação Trabalhista'
    ACAO_PREVIDENCIARIA = 'ACAO_PREVIDENCIARIA', 'Ação Previdenciária'
    SEGURO_DE_VIDA_PROPRIO = 'SEGURO_DE_VIDA_PROPRIO', 'Seguro de Vida Próprio'
    SEGURO_CONDUTOR = 'SEGURO_CONDUTOR', 'Seguro Condutor'
    SEGURO_DE_VIDA_EMPRESARIAL = (
        'SEGURO_DE_VIDA_EMPRESARIAL',
        'Seguro de Vida Empresarial',
    )
    SEGURO_DE_VIDA_NO_BANCO = 'SEGURO_DE_VIDA_NO_BANCO', 'Seguro de Vida no Banco'


class Attendance(ModelBase):
    customer_name = models.CharField(max_length=128)
    document_id = models.CharField(
        null=True, blank=True, max_length=11, validators=[validate_document_id]
    )
    status = models.PositiveSmallIntegerField(choices=AttendanceStatus.choices)
    resume = models.TextField(null=True)
    status_resume = models.TextField(null=True)
    services_provided = MultiSelectField(
        null=True,
        max_length=124,
        max_choices=len(ServicesOffered.choices),
        choices=ServicesOffered.choices,
    )

    class Meta:
        ordering = ['-updated_at']


def upload_to(instance, filename):
    attendance_pk = instance.attendance.pk
    ext = filename.split('.')[-1]
    new_filename = f'{uuid.uuid4()}.{ext}'
    return f'documentos/{attendance_pk}/{new_filename}'


class AttendanceFile(ModelBase):
    attendance = models.ForeignKey(
        Attendance, on_delete=models.CASCADE, related_name='files'
    )
    file = models.FileField(null=False, upload_to=upload_to, storage=MediaStorage())
    filename = models.CharField(null=False, max_length=124)
