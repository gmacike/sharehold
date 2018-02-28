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

# Create your views here.
