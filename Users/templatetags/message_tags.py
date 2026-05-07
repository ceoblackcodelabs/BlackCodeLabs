from django import template
from django.contrib import messages

register = template.Library()

@register.filter
def message_icon(tags):
    icon_map = {
        'success': 'fas fa-check-circle',
        'error': 'fas fa-exclamation-circle',
        'warning': 'fas fa-exclamation-triangle',
        'info': 'fas fa-info-circle',
        'debug': 'fas fa-bug'
    }
    return icon_map.get(tags, 'fas fa-info-circle')

@register.filter
def message_title(tags):
    title_map = {
        'success': 'Success!',
        'error': 'Error!',
        'warning': 'Warning!',
        'info': 'Information',
        'debug': 'Debug'
    }
    return title_map.get(tags, 'Information')