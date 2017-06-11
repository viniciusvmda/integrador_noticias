from django import template

register = template.Library()

@register.filter
def separator(value):
    return value.replace(" ", "_space_sep_")