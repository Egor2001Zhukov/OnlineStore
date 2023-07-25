# main/templatetags/my_tags.py

import datetime
from django import template

register = template.Library()


# Создание фильтра
@register.filter()
def mediapath(val):
    if val:
        return f'/media/{val}'
    return ''


@register.simple_tag()
def mediapath(val):
    if val:
        return f'/media/{val}'
    return ''
