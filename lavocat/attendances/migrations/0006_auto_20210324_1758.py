# Generated by Django 3.1.7 on 2021-03-24 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendances', '0005_auto_20210324_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Documentação Pendente'), (2, 'Documentação Parcial'), (3, 'À Contatar'), (4, 'Concluído')]),
        ),
    ]
