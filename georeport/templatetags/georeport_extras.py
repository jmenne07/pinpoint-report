from django import template

register = template.Library()


def key(value, arg):
    """
    Custom templatetag to access dictionaries in templates
    """
    return value[arg]


register.filter("key", key)
