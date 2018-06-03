from django.conf import settings
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from dal import autocomplete

from django.db.models.functions import Lower
from warehouse.forms import WarehouseForm, BoardGameContainerForm
from warehouse.models import Warehouse, BoardGameContainer


class WarehouseListView(LoginRequiredMixin, ListView):
    model = Warehouse
    # permission_required = 'warehouse.add_warehouse'
    raise_exception=True

    def get_queryset(self):
        return Warehouse.objects.all()

class WarehouseDetailView(LoginRequiredMixin, PermissionRequiredMixin, SingleObjectMixin, ListView):
    model = Warehouse
    permission_required = 'warehouse.add_warehouse'
    raise_exception=True
    template_name = 'warehouse/warehouse_detail.html'
    paginate_by = settings.WAREHOUSE_PAGINATION
    paginate_orphans = settings.WAREHOUSE_PAGINATION_ORPHANS
    # ListView context object => list of warehouse containers
    # context_object_name = 'warehouse_containers'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Warehouse.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['warehouse'] = self.object
        return context

    def get_queryset(self):
        if self.request.method == 'GET':
            if self.request.GET.__contains__("filter"):
                filter_criteria = self.request.GET.get("filter")
                self.request.session ['warehouse_filter'] = filter_criteria
            else:
                filter_criteria = self.request.session.get('warehouse_filter', None)
            if filter_criteria != None:
                containers_by_barcode = self.object.containers.filter(commodity__codeValue__icontains=filter_criteria)
                containers_by_label =  self.object.containers.filter(commodity__catalogueEntry__itemLabel__icontains=filter_criteria)
                contaiers_filtered = containers_by_barcode | containers_by_label
                self.queryset = contaiers_filtered.order_by(Lower("commodity__catalogueEntry__itemLabel"))
                # self.queryset = games_filtered.order_by(Lower("itemLabel"))
            else:
                self.queryset = self.object.containers.all().order_by(Lower("commodity__catalogueEntry__itemLabel"))
        # return self.object.containers.all()
        return self.queryset

# @login_required
# @permission_required('warehouse', raise_exception=True)
class WarehouseAutocompleteView(LoginRequiredMixin, PermissionRequiredMixin, autocomplete.Select2QuerySetView):
    permission_required = 'warehouse.add_warehouse'

    def get_queryset(self):
        qs = Warehouse.objects.all().order_by(Lower('itemLabel'))

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs

@login_required
def warehouse_select (request, *args, **kwargs):
    try:
        selected_warehouse = Warehouse.objects.get (pk=kwargs.pop('wrhpk'))
        if selected_warehouse:
            request.session ['warehouse_context_pk'] = selected_warehouse.pk
    except Warehouse.DoesNotExist as exc:
        messages.add_message(request, messages.ERROR, exc)
        raise Http404
    return redirect ('warehouse_index')

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
                # TODO: who did what to be registered
                container.save()
    except BoardGameContainer.DoesNotExist as exc:
        messages.add_message(request, messages.ERROR, exc)
        raise Http404

    return redirect ('warehouse_inventory', pk=container.warehouse.pk)


class WarehouseCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'warehouse.add_warehouse'
    raise_exception=True
    model = Warehouse
    form_class = WarehouseForm


class BoardGameContainerCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'warehouse.add_boardgamecontainer'
    raise_exception=True
    model = BoardGameContainer
    form_class = BoardGameContainerForm

    def get_initial(self):
        return {'warehouse': Warehouse.objects.get(pk=self.kwargs['pk'])}

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('warehouse_inventory', kwargs={'pk': pk})
