from django.views.generic import ListView, DetailView, CreateView

from warehouse.forms import WarehouseForm, ContainerForm
from warehouse.models import Warehouse, Container


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

# Create your views here.
