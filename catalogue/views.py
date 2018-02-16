from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.mixins import LoginRequiredMixin
from catalogue.models import (CatalogueItem, BoardGameItem)
from catalogue.forms import BoardGameForm
from django.views.generic import (ListView,DetailView,CreateView, UpdateView)

# Create your views here.
class CatalogueItemListView(ListView):
    model = BoardGameItem

    def get_queryset(self):
        return BoardGameItem.objects.all().order_by("itemLabel")

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
    form_class = BoardGameForm
    model = BoardGameItem

##########################################
def repeat_add_boardgame(request):
    if request.method == 'POST':
        form = BoardGameForm(request.POST)
        if form.is_valid():
            boardgame = form.save(commit=False)
            boardgame.save()
    return redirect('boardgame_new')

def boardgamelist_return(request):
    if request.method == 'POST':
        form = BoardGameForm(request.POST)
        if form.is_valid():
            boardgame = form.save(commit=False)
            boardgame.save()
    return redirect('catalogue_entries')
