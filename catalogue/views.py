from catalogue.models import (CatalogueItem, BoardGameItem, Warehouse, Container)
from catalogue.forms import BoardGameForm, WarehouseForm, ContainerForm

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import (ListView,DetailView,CreateView, UpdateView)

# Create your views here.
class CatalogueItemListView(ListView):
    queryset = BoardGameItem.objects.all().order_by("itemLabel")
    filter_criteria = ""
    context_object_name = 'catalogueitem_list'
    template_name = 'catalogue/catalogueitem_list.html'
    paginate_by = 4
    paginate_orphans = 2


    def get_queryset(self):
        if self.request.method == 'GET':

            self.filter_criteria = self.request.GET.get("filter")
            if self.filter_criteria:
                search_type = self.request.GET.get("search")
                if search_type == "barcode":
                    self.queryset = BoardGameItem.objects.filter(codeValue__startswith=self.filter_criteria).order_by("codeValue")
                elif search_type == "title":
                    self.queryset =  BoardGameItem.objects.filter(itemLabel__icontains=self.filter_criteria).order_by("itemLabel")
                # else:
                #     objects =  self.model.objects.all().order_by("-itemLabel")
            return self.queryset


# class CatalogueItemFilteredListView(CatalogueItemListView):
#     filterCriteria = ""
#     def get_queryset(self):
#         return BoardGameItem.objects.all().order_by("itemLabel")


class BoardGameDetailsView(DetailView):
    model = BoardGameItem

class BoardGameCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    #authorization restriction section
    # login_url = 'accounts/login/'
    permission_required = 'catalogue.add_boardgameitem'
    raise_exception=True

    form_class = BoardGameForm
    model = BoardGameItem

class BoardGameUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    #authorization restriction section
    permission_required = 'catalogue.change_boardgameitem'
    raise_exception=True
    # login_url = 'accounts/login/'

    form_class = BoardGameForm
    model = BoardGameItem


class WarehouseListView(ListView):
    model = Warehouse

    def get_queryset(self):
        return Warehouse.objects.all()


class WarehouseDetailView(DetailView):
    model = Warehouse


class WarehouseCreateView(CreateView):
    model = Warehouse
    form_class = WarehouseForm


class ContainerCreateView(CreateView):
    model = Container
    form_class = ContainerForm

##########################################
# BoardGameItem additional views
##########################################
@login_required
@permission_required('catalogue.add_boardgameitem', raise_exception=True)
def repeat_add_boardgame(request):
    if request.method == 'POST':
        form = BoardGameForm(request.POST)
        if form.is_valid():
            boardgame = form.save(commit=False)
            boardgame.save()
    return redirect('boardgame_new')

@login_required
@permission_required('catalogue.add_boardgameitem', raise_exception=True)
def boardgamelist_return(request):
    if request.method == 'POST':
        form = BoardGameForm(request.POST)
        if form.is_valid():
            boardgame = form.save(commit=False)
            boardgame.save()
    return redirect('catalogue_entries')

@login_required
@permission_required('catalogue.add_boardgameitem', raise_exception=True)
def return_home (request):
    if request.method == 'POST':
        form = BoardGameForm(request.POST)
        if form.is_valid():
            boardgame = form.save(commit=False)
            boardgame.save()
    return redirect('welcome')

