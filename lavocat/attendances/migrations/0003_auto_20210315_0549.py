# Generated by Django 3.1.7 on 2021-03-15 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendances', '0002_auto_20210315_0524'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attachment',
            old_name='attachment',
            new_name='file',
        ),
    ]