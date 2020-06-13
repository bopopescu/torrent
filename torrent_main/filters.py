import django_filters

import django_filters

from torrent_main import models


class TorrentSortingFilter(django_filters.FilterSet):

    ORDER_CHOICE = (
        ('date_uploaded', 'Sort by Time'),
        ('total_size', 'Sort by Size'),
        ('seeders', 'Sort by Seeders'),
        ('leeches', 'Sort by Leeches'),

    )

    sorting = django_filters.ChoiceFilter(label='sorting',
                                          choices=ORDER_CHOICE,
                                          method='filter_by_order')

    class Meta:
        model = models.Torrent
        fields = ('sorting', )

    def filter_by_order(self, queryset, name, value):
        expression = '-' + value
        return queryset.order_by(expression)