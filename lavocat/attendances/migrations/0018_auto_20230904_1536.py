# Generated by Django 3.1.7 on 2023-09-04 15:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('attendances', '0017_attendance_services_provided'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.PositiveSmallIntegerField(
                choices=[
                    (1, 'Documentação pendente'),
                    (2, 'Em andamento'),
                    (3, 'À contatar'),
                    (4, 'Concluído'),
                ],
                null=True,
            ),
        ),
    ]