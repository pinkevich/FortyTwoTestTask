from django.db.models.base import Model
from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def edit_link(obj):
    """
    :param obj: model instance object
    :return: safe link for edit instance in admin
    """
    if not isinstance(obj, Model):
        raise template.TemplateSyntaxError(
            '{} is not model instance'.format(obj)
        )
    info = obj._meta.app_label, obj._meta.model_name
    url = reverse('admin:%s_%s_change' % info, args=(obj.pk,))
    return mark_safe('<a href="{0}">{1}</a>'.format(url, obj))
