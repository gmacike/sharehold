from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

from warehouse.forms import WarehouseForm, BoardGameContainerForm
from warehouse.models import Warehouse, BoardGameContainer


class WarehouseListView(ListView):
    model = Warehouse
    permission_required = 'warehouse'
    raise_exception=True

    def get_queryset(self):
        return Warehouse.objects.all()


class WarehouseDetailView(DetailView):
    model = Warehouse
    permission_required = 'warehouse'
    raise_exception=True

@login_required
@permission_required('warehouse.change_boardgamecontainer', raise_exception=True)
def bgcontainer_inc (request, *args, **kwargs):

    try:
        container = BoardGameContainer.objects.get (pk=kwargs.pop('cntpk'))
        if container:
            container.total += 1
            container.save()
    except BoardGameContainer.DoesNotExist as exc:
        messages.add_message(request, messages.ERROR, exc)
        raise Http404

    return redirect ('warehouse_inventory', pk=container.warehouse.pk)

@login_required
@permission_required('warehouse.change_boardgamecontainer', raise_exception=True)
def bgcontainer_dec (request, *args, **kwargs):

    try:
        container = BoardGameContainer.objects.get (pk=kwargs.pop('cntpk'))
        if container:
            if container.total > 0:
                container.total -= 1
                container.save()
    except BoardGameContainer.DoesNotExist as exc:
        messages.add_message(request, messages.ERROR, exc)
        raise Http404

    return redirect ('warehouse_inventory', pk=container.warehouse.pk)


class WarehouseCreateView(CreateView):
    permission_required = 'warehouse.add_warehouse'
    raise_exception=True
    model = Warehouse
    form_class = WarehouseForm


class BoardGameContainerCreateView(CreateView):
    permission_required = 'warehouse.add_boardgamecontainer'
    raise_exception=True
    model = BoardGameContainer
    form_class = BoardGameContainerForm

    def get_initial(self):
        return {'warehouse': Warehouse.objects.get(pk=self.kwargs['pk'])}

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('warehouse_detail', kwargs={'pk': pk})
