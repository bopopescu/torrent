# Generated by Django 3.0.4 on 2020-05-21 18:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('torrent_main', '0011_auto_20200516_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='torrent',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_created=True)),
                ('text', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('torrent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='torrent_main.Torrent')),
            ],
        ),
    ]
