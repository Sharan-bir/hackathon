# Generated by Django 5.0.3 on 2025-04-29 18:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crime_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_station_head',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='managed_station',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='policemen', to='crime_api.policestation'),
        ),
        migrations.AlterField(
            model_name='policestation',
            name='head',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='headed_station', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='policestation',
            name='location',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.IntegerField(choices=[(1, 'User'), (2, 'Police'), (3, 'Department')], default=1),
        ),
    ]
