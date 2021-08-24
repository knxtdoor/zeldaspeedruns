from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

import markdown

register = template.Library()


@register.filter(name='markdown', needs_autoescape=True)
def convert_markdown(value, autoescape=True):
    if autoescape:
        return mark_safe(conditional_escape(markdown.markdown(value)))
    else:
        return mark_safe(markdown.markdown(value))
