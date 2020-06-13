from django.template import Library

from torrent_main import models


register = Library()


@register.simple_tag
def get_categories():
    cat_list = models.Category.objects.all()
    return cat_list


