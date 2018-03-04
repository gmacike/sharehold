from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView

from warehouse.forms import WarehouseForm, BoardGameContainerForm
from warehouse.models import Warehouse, BoardGameContainer


class WarehouseListView(ListView):
    model = Warehouse

    def get_queryset(self):
        return Warehouse.objects.all()


class WarehouseDetailView(DetailView):
    model = Warehouse


class WarehouseCreateView(CreateView):
    model = Warehouse
    form_class = WarehouseForm


class BoardGameContainerCreateView(CreateView):
    model = BoardGameContainer
    form_class = BoardGameContainerForm

    def get_initial(self):
        return {'warehouse': Warehouse.objects.get(pk=self.kwargs['pk'])}

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('warehouse_detail', kwargs={'pk': pk})

# Create your views here.
