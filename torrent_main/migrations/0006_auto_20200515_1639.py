# Generated by Django 3.0.4 on 2020-05-15 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('torrent_main', '0005_auto_20200406_1958'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TorrentFileInfo',
            new_name='TorrentFilesInfo',
        ),
        migrations.AlterField(
            model_name='torrent',
            name='file',
            field=models.FileField(upload_to='torrent_files'),
        ),
        migrations.AlterField(
            model_name='torrent',
            name='image',
            field=models.ImageField(default=1, upload_to='torrent_images'),
            preserve_default=False,
        ),
    ]
