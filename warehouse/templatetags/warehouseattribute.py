from django import template
from warehouse.models import Warehouse

register = template.Library()

@register.simple_tag
def get_warehouse_attribute (wrhpk, attribute):
    """
    get Warehouse object of given pk and retrieve its requested attribute value
    """
    try:
        selected_warehouse = Warehouse.objects.get (pk=wrhpk)
        value = getattr(selected_warehouse, attribute)
    except Warehouse.DoesNotExist as exc:
        messages.add_message(request, messages.ERROR, exc)
        raise Http404

    return value

# register.inclusion_tag('paginator.html', takes_context=False)(get_warehouse_attributes)
