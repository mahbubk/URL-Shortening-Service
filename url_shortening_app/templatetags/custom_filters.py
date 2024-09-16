from django import template

register = template.Library()


@register.filter(name='build_absolute_uri')
def build_absolute_uri(request, short_code):
    return request.build_absolute_uri(short_code)