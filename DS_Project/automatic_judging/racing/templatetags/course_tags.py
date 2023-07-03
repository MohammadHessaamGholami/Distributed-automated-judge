from django import template
from django.contrib import messages

register = template.Library()


@register.filter
def type_of_noty(message):
    types = {messages.ERROR: "error",
             messages.WARNING: "warning",
             messages.INFO: "information",
             messages.SUCCESS: "success"
             }
    return types.get(message.level)
