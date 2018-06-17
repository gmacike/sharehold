# taken from https://djangosnippets.org/snippets/73/
# use in template by inserting:
# {% load pagination %}
# {% paginator %} 

from django import template
register = template.Library()

def paginator(context, adjacent_pages=2, show_far_away_pages=True, far_away_step=10):
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
    if show_far_away_pages:
        far_away_page = current_page + far_away_step
        far_behind_page = current_page - far_away_step
    else:
        far_away_page = number_of_pages
        far_behind_page = 1
    page_numbers = [n for n in range(startPage, endPage) \
        if 0 < n <= number_of_pages]

    return {
        'page_obj': page_obj,
        'paginator': paginator,
        'page': current_page,
        'pages': number_of_pages,
        'page_numbers': page_numbers,
        'has_far_behind': far_behind_page > 1,
        'far_behind_page': far_behind_page,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'has_far_away': far_away_page < number_of_pages,
        'far_away_page': far_away_page,
        'show_first': 1 != current_page,
        'show_last': number_of_pages != current_page,
    }

register.inclusion_tag('paginator.html', takes_context=True)(paginator)
