from django.shortcuts import render
# from django.contrib.auth.mixins import LoginRequiredMixin
from catalogue.models import (CatalogueItem, BoardGameItem)
from catalogue.forms import BoardGameForm
from django.views.generic import (ListView,DetailView,CreateView, UpdateView)

# Create your views here.
class CatalogueItemListView(ListView):
    model = CatalogueItem

    def get_queryset(self):
        return CatalogueItem.objects
        # .orderby('itemLabel')

class BoardGameDetailsView(DetailView):
    model = BoardGameItem

# todo: add LoginRequiredMixin inheritance
class BoardGameCreateView(CreateView):
    #authorization restriction section
    # login_url = '/login/'
    # redirect_field_name = todo define it

    form_class = BoardGameForm
    model = BoardGameItem

# todo: add LoginRequiredMixin inheritance
class BoardGameUpdateView(UpdateView):
    #authorization restriction section
    # login_url = '/login/'
    # redirect_field_name = todo define it

    model = BoardGameItem
