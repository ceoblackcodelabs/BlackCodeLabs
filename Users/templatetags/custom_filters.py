from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """
    Split a string by the given argument
    Usage: {{ value|split:"arg" }}
    """
    if value:
        return value.split(arg)
    return []

@register.filter
def get_item(dictionary, key):
    """
    Get a value from a dictionary by key
    Usage: {{ dictionary|get_item:key }}
    """
    return dictionary.get(key)

@register.filter
def contains(value, arg):
    """
    Check if value contains arg
    Usage: {% if list|contains:item %}
    """
    return arg in value if value else False