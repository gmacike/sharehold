from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from catalogue.models import (CatalogueItem, BoardGameItem, BoardGameCommodity)
from catalogue.forms import BoardGameItemForm, BoardGameCommodityForm
from django.views.generic import (ListView,DetailView,CreateView, UpdateView)
from django.conf import settings
from dal import autocomplete
# for case insensitive qureyset ordering
from django.db.models.functions import Lower
from warehouse.models import BoardGameContainer

# Create your views here.
class CatalogueItemListView(ListView):
    queryset = BoardGameItem.objects.all().order_by(Lower("itemLabel"))
    # filter_criteria = ""
    context_object_name = 'catalogueitem_list'
    template_name = 'catalogue/catalogueitem_list.html'
    paginate_by = settings.CATALOGUE_PAGINATION
    paginate_orphans = settings.CATALOGUE_PAGINATION_ORPHANS


    def get_queryset(self):
        self.queryset = BoardGameItem.objects.none()
        if self.request.method == 'GET':
            if self.request.GET.__contains__("filter"):
                filter_criteria = self.request.GET.get("filter")
                self.request.session ['catalogue_filter'] = filter_criteria
            else:
                filter_criteria = self.request.session.get ('catalogue_filter', None)
            if filter_criteria != None:
                commodities_ids = BoardGameCommodity.objects.filter(codeValue__icontains=filter_criteria).values_list('catalogueEntry')
                games_by_barcode = BoardGameItem.objects.filter(id__in=commodities_ids)
                games_by_title = BoardGameItem.objects.filter(itemLabel__icontains=filter_criteria)
                games_filtered = games_by_barcode | games_by_title
                self.queryset = games_filtered.order_by(Lower("itemLabel"))
            else:
                self.queryset = BoardGameItem.objects.all().order_by("itemLabel")
            return self.queryset

class BoardGameItemDetailsView(DetailView):
    model = BoardGameItem

class BoardGameItemCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    #authorization restriction section
    # login_url = 'accounts/login/'
    permission_required = 'catalogue.add_boardgameitem'
    raise_exception=True

    form_class = BoardGameItemForm
    model = BoardGameItem

class BoardGameItemUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    #authorization restriction section
    permission_required = 'catalogue.change_boardgameitem'
    raise_exception=True
    # login_url = 'accounts/login/'

    form_class = BoardGameItemForm
    model = BoardGameItem

##########################################
# BoardGameItem additional views
##########################################
@login_required
@permission_required('catalogue.add_boardgameitem', raise_exception=True)
def repeat_add_boardgame(request):
    if request.method == 'POST':
        form = BoardGameItemForm(request.POST)
        if form.is_valid():
            boardgame = form.save(commit=False)
            boardgame.save()
    return redirect('boardgame_new')

@login_required
@permission_required('catalogue.add_boardgameitem', raise_exception=True)
def boardgamelist_return(request):
    if request.method == 'POST':
        form = BoardGameItemForm(request.POST)
        if form.is_valid():
            boardgame = form.save(commit=False)
            boardgame.save()
    return redirect('catalogue_entries')


@login_required
@permission_required('catalogue.add_boardgameitem', raise_exception=True)
def return_home (request):
    if request.method == 'POST':
        form = BoardGameItemForm(request.POST)
        if form.is_valid():
            boardgame = form.save(commit=False)
            boardgame.save()
    return redirect('welcome')

class BoardGameAutocompleteView(autocomplete.Select2QuerySetView):
    # these queryset data will be available through pulib url guard w/ permissions if necessary
    # here are none as boardgame cataloge is going to be available for publicity
    def get_queryset(self):
        qs = BoardGameItem.objects.all().order_by(Lower('itemLabel'))

        if self.q:
            qs = qs.filter(itemLabel__icontains=self.q)

        return qs


class BoardGameCommodityCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    #authorization restriction section
    # login_url = 'accounts/login/'
    permission_required = 'catalogue.add_boardgamecommodity'
    raise_exception=True

    form_class = BoardGameCommodityForm
    model = BoardGameCommodity
    template_name = 'catalogue/boardgamecommodity_form.html'

    initial = {}

    def get(self, request, *args, **kwargs):
        if 'bgpk' in kwargs:
            self.initial ['catalogueEntry'] = kwargs ['bgpk']
        else:
            self.initial ['catalogueEntry'] = None
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

class BoardGameCommodityUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    #authorization restriction section
    permission_required = 'catalogue.change_boardgamecommodity'
    raise_exception=True
    # login_url = 'accounts/login/'

    form_class = BoardGameCommodityForm
    model = BoardGameCommodity

# TODO add PermissionRequiredMixin
class BoardGameCommodityNotInWarehouseAutocompleteViewByCode(autocomplete.Select2QuerySetView):
    # these queryset data will be available through pulib url guard w/ permissions if necessary
    # here are none as boardgame cataloge is going to be available for publicity
    warehouse = None

    def get_queryset(self):
        if self.q:
            qs = BoardGameCommodity.objects.filter(codeValue__icontains=self.q).order_by('codeValue')
        else:
            qs = BoardGameCommodity.objects.all().order_by('codeValue')

        return qs
