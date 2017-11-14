from django.template import Library
from django.contrib.contenttypes.models import ContentType

register = Library()


@register.filter_function
def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)


@register.assignment_tag
def content_type(obj):
    return ContentType.objects.get_for_model(obj)
