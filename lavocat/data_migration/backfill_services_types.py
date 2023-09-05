from lavocat.attendances.models import Attendance, ServicesTypesOptions

FROM_TO = (
    (['DPVAT'], ServicesTypesOptions.DPVAT),
    (['AUX DOENCA'], ServicesTypesOptions.AUXILIO_DOENCA),
    (['AUX ACIDENTE'], ServicesTypesOptions.AUXILIO_ACIDENTE),
    (['LOAS'], 'LOAS'),
    (
        ['CONTRA CONDUTOR', 'CONTRA PREFEITURA', 'AÇÃO CONTRA UPA'],
        ServicesTypesOptions.ACAO_INDENIZATORIA,
    ),
    (['TRABALHISTA'], ServicesTypesOptions.ACAO_TRABALHISTA),
    (
        ['SELETA', 'SEGURO CPFL', 'SEGUROS PRIVADOS (MAGAZINE'],
        ServicesTypesOptions.SEGURO_DE_VIDA_EMPRESARIAL,
    ),
    (
        ['SEGURO OUTRA PARTE', 'SEGURO DE 3', 'SEGUROS PRIVADOS (MAGAZINE'],
        ServicesTypesOptions.SEGURO_CONDUTOR,
    ),
)


for attendance in Attendance.objects.filter(status_resume__isnull=False):
    services = attendance.services_types
    for from_, to in FROM_TO:
        for item in from_:
            if item in attendance.status_resume and to not in services:
                services.append(to)
    attendance.services_types = services
    attendance.save()
