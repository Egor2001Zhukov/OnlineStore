# main/templatetags/my_tags.py

import datetime
from django import template
from django.contrib.auth.models import Group

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


@register.filter()
def is_moderator(val):
    moderators = Group.objects.get(name="moderators").user_set.all()
    if val in moderators:
        return True
    return False

@register.filter()
def is_content_moderator(val):
    moderators = Group.objects.get(name="content_moderators").user_set.all()
    if val in moderators:
        return True
    return False