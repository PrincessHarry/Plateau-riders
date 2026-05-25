from django import template

register = template.Library()


@register.filter
def split(value, sep=','):
    """Split a string by `sep` and return a list. If value is falsy, return an empty list."""
    if not value:
        return []
    try:
        return value.split(sep)
    except Exception:
        return []


@register.filter
def underscore_to_space(value):
    """Replace underscores with spaces in a string."""
    if value is None:
        return ''
    return str(value).replace('_', ' ')
