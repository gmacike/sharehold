from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.mixins import LoginRequiredMixin
from catalogue.models import (CatalogueItem, BoardGameItem, RentalClient)
from catalogue.forms import (BoardGameForm, RentalClientForm)
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
# BoardGameItem additional views
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
    
############################################
# Client Views
############################################

class RentalClientListView(ListView):
    model = RentalClient

    def get_queryset(self):
        return RentalClient.objects.all()
        # .orderby('itemLabel')
    
class RentalClientDetailsView(DetailView):
    model = RentalClient
    
class RentalClientCreateView(CreateView):
    #authorization restriction section
    # login_url = '/login/'
    # redirect_field_name = todo define it

    form_class = RentalClientForm
    model = RentalClient
