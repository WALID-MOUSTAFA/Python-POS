from django.template import Library

register = Library()

@register.simple_tag
def related_products(id):
    from Admin.models import Category
    return Category.related_products(id)
