# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0003_auto_20150502_1641'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='firstName',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='lastName',
            new_name='last_name',
        ),
    ]
