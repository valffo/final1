from django import template

register = template.Library()


@register.filter
def get(dictionary, key):
    return -dictionary.get(key, 0)


@register.filter
def minus(x, y):
    return x-y


@register.filter
def multiply(value, arg):
    return value*arg