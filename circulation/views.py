from urllib.parse import urlencode

from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from dal import autocomplete
from django.forms import inlineformset_factory
from circulation.models import (RentalClient, ClientID, BoardGameLending)
from warehouse.models import Warehouse, BoardGameContainer
from circulation.forms import (RentalClientForm, RentalClientIDInlineFormSet, BoardGameLendingForm)
from django.views.generic import (ListView, DetailView, CreateView, UpdateView)
from django.conf import settings


############################################
# Client Views
############################################
class RentalClientListView(ListView):
    model = RentalClient
    paginate_by = settings.CLIENTS_PAGINATION
    paginate_orphans = settings.CLIENTS_PAGINATION_ORPHANS

    def get_queryset(self):
        if self.request.method == 'GET':
            self.filter_criteria = self.request.GET.get("filter")
            if self.filter_criteria and len(self.filter_criteria) >= 2:
                search_type = self.request.GET.get("search")
                if search_type == "identificationCode":
                    return RentalClient.objects.filter(identificationCode__startswith=self.filter_criteria).order_by(
                        "identificationCode")
                elif search_type == "initials":
                    return RentalClient.objects.filter(initials__icontains=self.filter_criteria).order_by("initials")

        return RentalClient.objects.none()


class RentalClientDetailsView(DetailView):
    model = RentalClient


class RentalClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'circulation.add_rentalclient'
    form_class = RentalClientForm
    model = RentalClient


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'circulation.change_rentalclient'
    raise_exception = True

    form_class = RentalClientForm
    model = RentalClient


# @login_required
# @permission_required('warehouse', raise_exception=True)
class ClientAutocompleteViewByIDlabel(LoginRequiredMixin, PermissionRequiredMixin, autocomplete.Select2QuerySetView):
    permission_required = 'circulation.add_boardgamelending'

    def get_queryset(self):
        qs = RentalClient.objects.all().order_by('clientIDs__IDlabel')
        if self.q:
            qs = qs.filter(clientIDs__IDlabel__icontains=self.q)
        return qs


class BoardGameUpdate2View(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'circulation.change_rentalclient'
    raise_exception = True

    form_class = RentalClientForm
    model = RentalClient


@login_required
@permission_required('circulation.change_rentalclient', raise_exception=True)
def manage_rentalclient(request, pk):
    rentalClient = get_object_or_404(RentalClient, pk=pk)
    form = RentalClientForm(instance=rentalClient)
    RentalClientInlineFormSet = inlineformset_factory(RentalClient, ClientID, fields=('ID', 'active'), extra=1, formset=RentalClientIDInlineFormSet, can_delete=False)
    if request.method == "POST":
        formset = RentalClientInlineFormSet(request.POST, request.FILES, instance=rentalClient)
        if formset.is_valid():
            formset.save()
            return redirect_query('circulation_entries',
                                  {'filter': rentalClient.identificationCode, 'search': 'identificationCode'})
    else:
        formset = RentalClientInlineFormSet(instance=rentalClient)
    return render(request, 'circulation/rentalclient_details.html', {'form': form, 'formset': formset})


def redirect_query(url, params=None):
    response = redirect(url)
    if params:
        query_string = urlencode(params)
        response['Location'] += '?' + query_string
    return response

@login_required
@permission_required('circulation.add_rentalclient', raise_exception=True)
def addAndEditRentalClient(request):
    if request.method == 'POST':
        form = RentalClientForm(request.POST)
        if form.is_valid():
            rentalClient = form.save(commit=False)
            rentalClient.save()
            return redirect('rentalclient_details', pk=rentalClient.pk)
        else:
            return render(request, 'circulation/rentalclient_form.html', {'form': form})
    return redirect('circulation_entries')

@login_required
@permission_required('circulation.add_rentalclient', raise_exception=True)
def addAndReturn_rentalClientList(request):
    if request.method == 'POST':
        form = RentalClientForm(request.POST)
        if form.is_valid():
            rentalClient = form.save(commit=False)
            rentalClient.save()
            return redirect_query('circulation_entries',
                                  {'filter': rentalClient.identificationCode, 'search': 'identificationCode'})
        else:
            return render(request, 'circulation/rentalclient_form.html', {'form': form})
    return redirect('circulation_entries')


@login_required
@permission_required('circulation.add_rentalclient', raise_exception=True)
def addAndAddNew_rentalClientList(request):
    if request.method == 'POST':
        form = RentalClientForm(request.POST)
        if form.is_valid():
            rentalClient = form.save(commit=False)
            rentalClient.save()
            return redirect_query('rentalClient_new')
        else:
            return render(request, 'circulation/rentalclient_form.html', {'form': form})
    return redirect('rentalClient_new')


@login_required
@permission_required('circulation.change_rentalclient', raise_exception=True)
def updateAndReturn_rentalClientList(request, pk):
    if request.method == 'POST':
        client = get_object_or_404(RentalClient, pk=pk)
        form = RentalClientForm(request.POST, instance=client)
        if form.is_valid():
            rentalClient = form.save(commit=False)
            rentalClient.save()
            return redirect_query('circulation_entries',
                                  {'filter': rentalClient.identificationCode, 'search': 'identificationCode'})
        else:
            return render(request, 'circulation/rentalclient_form.html', {'form': form, 'rentalclient': client})
    return redirect('circulation_entries')


class BoardGameLendingList(ListView):
    model = BoardGameLending


class BoardGameLendingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = BoardGameLending
    permission_required = 'circulation.add_boardgamelending'
    raise_exception=True
    form_class = BoardGameLendingForm


class BoardGameLendingDetailView(DetailView):
    model = BoardGameLending


def register_return(request, pk):
    if request.method == 'POST':
        BoardGameLending = get_object_or_404(BoardGameLending, pk=pk)
        BoardGameLending.returned = datetime.now()
        BoardGameLending.save()

    return redirect('BoardGameLending_detail', pk=pk)


# TODO add PermissionRequiredMixin
class BoardGameContainerInWarehouseAutocompleteViewByCommodity(autocomplete.Select2QuerySetView):
    # these queryset data will be available through pulib url guard w/ permissions if necessary
    # here are none as boardgame cataloge is going to be available for publicity

    def get_queryset(self):
        selected_warehouse = None
        warehouse_pk = None

        if self.request.method == 'GET':
            if self.request.GET.__contains__("wrhpk"):
                warehouse_pk = self.request.GET.get("wrhpk")
            else:
                warehouse_pk = self.request.session.get('warehouse_context_pk', None)

        if warehouse_pk != None:
            try:
                selected_warehouse = Warehouse.objects.get (pk=warehouse_pk)
            except Warehouse.DoesNotExist as exc:
                messages.add_message(request, messages.ERROR, exc)
                raise Http404

            if self.q:
                qs = BoardGameContainer.objects.filter(warehouse=selected_warehouse,
                    commodity__codeValue__icontains=self.q).order_by('commodity__codeValue')
            else:
                qs = BoardGameContainer.objects.filter(warehouse=selected_warehouse).order_by('codeValue')
        else:
            qs = BoardGameContainer.objects.none()

        return qs
