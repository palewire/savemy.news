from django import template
from django.template.defaultfilters import truncatechars
register = template.Library()


@register.filter
def trimurl(value):
    value = value.replace("http://", "")
    value = value.replace("https://", "")
    value = truncatechars(value, 70)
    return value
