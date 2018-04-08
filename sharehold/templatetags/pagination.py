# taken from https://djangosnippets.org/snippets/73/
# use in template by inserting:
# {% load pagination %}
# {% paginator 5 %}

from django import template
register = template.Library()

def paginator(context, adjacent_pages=2):
    """
    To be used in conjunction with the object_list generic view.

    Adds pagination context variables for use in displaying first, adjacent and
    last page links in addition to those created by the object_list generic
    view.

    """
    current_page = context['page_obj'].number
    number_of_pages = context['paginator'].num_pages
    page_obj = context['page_obj']
    paginator = context['paginator']
    startPage = max(current_page - adjacent_pages, 1)
    endPage = current_page + adjacent_pages + 1
    if endPage > number_of_pages: endPage = number_of_pages + 1
    page_numbers = [n for n in range(startPage, endPage) \
        if 0 < n <= number_of_pages]

    return {
        'page_obj': page_obj,
        'paginator': paginator,
        'page': current_page,
        'pages': number_of_pages,
        'page_numbers': page_numbers,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'show_first': 1 != current_page,
        'show_last': number_of_pages != current_page,
    }

register.inclusion_tag('paginator.html', takes_context=True)(paginator)
