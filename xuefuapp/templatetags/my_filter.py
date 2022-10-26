#coding=utf-8
from django import template
from json import loads
register = template.Library()

@register.filter
def or_blank(value):
    return value if value else ''

