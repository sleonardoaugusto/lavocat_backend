# Generated by Django 3.1.7 on 2021-03-25 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendances', '0006_auto_20210324_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='resume',
            field=models.TextField(null=True),
        ),
    ]
