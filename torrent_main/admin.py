from django.contrib import admin

from torrent_main import models

admin.site.register(models.Type)
admin.site.register(models.Category)
# admin.site.register(models.TorrentFileInfo)


class CustomTorrentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'uploaded_by', 'downloads', 'last_checked',
                    'is_pub')
    # exclude = ('slug', 'total_size', 'last_checked', 'seeders', 'leeches', 'link')
    list_filter = ('date_uploaded', 'is_pub')


admin.site.register(models.Torrent, CustomTorrentAdmin)
