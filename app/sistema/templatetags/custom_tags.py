from django import template
from rest_framework.utils.serializer_helpers import ReturnList
from django.db.models.query import QuerySet
from collections import OrderedDict

register = template.Library()

@register.filter
def is_in(value, list_obj):
    if not list_obj:
        return False

    if isinstance(list_obj, ReturnList):
        response = any(value == obj['id'] if isinstance(obj, OrderedDict) else obj.id for obj in list_obj)
    elif isinstance(list_obj, QuerySet):
        response = any(value == obj.id for obj in list_obj.all())
    else:
        raise ValueError("Invalid input type. Expected ReturnList or QuerySet.")
    return response

