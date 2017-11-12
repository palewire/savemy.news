from django import template
from django.template.defaultfilters import truncatechars
register = template.Library()


@register.filter
def trimurl(value):
    value = value.replace("http://", "")
    value = value.replace("https://", "")
    value = value.replace("www.", "")
    value = truncatechars(value, 65)
    return value
