# Generated by Django 3.0.4 on 2020-05-15 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('torrent_main', '0007_auto_20200515_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='torrent',
            name='info_hash',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
