# Generated by Django 3.0.4 on 2020-03-31 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('torrent_main', '0003_auto_20200331_1610'),
    ]

    operations = [
        migrations.CreateModel(
            name='TorrentFileInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.FloatField()),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='torrent',
            name='file',
            field=models.FileField(default='asd', upload_to='torrent_files'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='TorrentFile',
        ),
        migrations.AddField(
            model_name='torrentfileinfo',
            name='torrent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='torrent_main.Torrent'),
        ),
    ]
