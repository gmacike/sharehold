from urllib.parse import urlencode

from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from dal import autocomplete
from django.forms import inlineformset_factory
from circulation.models import (Customer, CustomerID, BoardGameLending)
from warehouse.models import Warehouse, BoardGameContainer
from circulation.forms import (CustomerForm, RentalCustomerIDInlineFormSet, BoardGameLendingForm)
from django.views.generic import (ListView, DetailView, CreateView, UpdateView)
from django.conf import settings
from sharehold.templatetags.anypermission import has_any_permission


@login_required
@has_any_permission (('circulation.add_boardgamelending', 'circulation.change_boardgamelending',
    'circulation.add_customer', 'circulation.change_customer'))
def circulation_home(request):
    if request.user.has_perm ('circulation.add_boardgamelending') or request.user.has_perm('circulation.change_boardgamelending'):
        return redirect('circulation_lend')

    if request.user.has_perm ('circulation.add_customer') or request.user.has_perm('circulation.change_customer'):
        return redirect('circulation_newcustomer')
    return redirect('circulation_newcustomer')


############################################
# Client Views
############################################
# class CustomerListView(ListView):
#     model = Customer
#     paginate_by = settings.CLIENTS_PAGINATION
#     paginate_orphans = settings.CLIENTS_PAGINATION_ORPHANS
#
#     def get_queryset(self):
#         if self.request.method == 'GET':
#             self.filter_criteria = self.request.GET.get("filter")
#             if self.filter_criteria and len(self.filter_criteria) >= 2:
#                 search_type = self.request.GET.get("search")
#                 if search_type == "identificationCode":
#                     return Customer.objects.filter(identificationCode__startswith=self.filter_criteria).order_by(
#                         "identificationCode")
#                 elif search_type == "initials":
#                     return Customer.objects.filter(initials__icontains=self.filter_criteria).order_by("initials")
#
#         return Customer.objects.none()
#
#
# class CustomerDetailsView(DetailView):
#     model = Customer
#
#
class CustomerCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'circulation.add_customer'
    form_class = CustomerForm
    model = Customer


class CustomerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'circulation.change_customer'
    raise_exception = True

    form_class = CustomerForm
    model = Customer


# @login_required
# @permission_required('warehouse', raise_exception=True)
class ClientAutocompleteViewByIDlabel(LoginRequiredMixin, PermissionRequiredMixin, autocomplete.Select2QuerySetView):
    permission_required = 'circulation.add_boardgamelending'

    def get_queryset(self):
        qs = Customer.objects.all().order_by('CustomerIDs__IDlabel')
        if self.q:
            qs = qs.filter(CustomerIDs__IDlabel__icontains=self.q)
        return qs


class BoardGameUpdate2View(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'circulation.change_Customer'
    raise_exception = True

    form_class = CustomerForm
    model = Customer

#
# @login_required
# @permission_required('circulation.change_customer', raise_exception=True)
# def manage_Customer(request, pk):
#     Customer = get_object_or_404(Customer, pk=pk)
#     form = CustomerForm(instance=Customer)
#     CustomerInlineFormSet = inlineformset_factory(Customer, CustomerID, fields=('ID', 'active'), extra=1, formset=RentalCustomerIDInlineFormSet, can_delete=False)
#     if request.method == "POST":
#         formset = CustomerInlineFormSet(request.POST, request.FILES, instance=Customer)
#         if formset.is_valid():
#             formset.save()
#             return redirect_query('circulation_newcustomer',
#                                   {'filter': Customer.identificationCode, 'search': 'identificationCode'})
#     else:
#         formset = CustomerInlineFormSet(instance=Customer)
#     return render(request, 'circulation/circulation_customerdetails.html', {'form': form, 'formset': formset})
#
#
# def redirect_query(url, params=None):
#     response = redirect(url)
#     if params:
#         query_string = urlencode(params)
#         response['Location'] += '?' + query_string
#     return response

@login_required
@permission_required('circulation.add_customer', raise_exception=True)
def repeat_add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            Customer = form.save(commit=False)
            Customer.save()
        else:
            return render(request, 'circulation/customer_form.html', {'form': form})
    return redirect('circulation_newcustomer')
#
# @login_required
# @permission_required('circulation.add_customer', raise_exception=True)
# def addAndReturn_CustomerList(request):
#     if request.method == 'POST':
#         form = CustomerForm(request.POST)
#         if form.is_valid():
#             Customer = form.save(commit=False)
#             Customer.save()
#             return redirect_query('circulation_newcustomer',
#                                   {'filter': Customer.identificationCode, 'search': 'identificationCode'})
#         else:
#             return render(request, 'circulation/customer_form.html', {'form': form})
#     return redirect('circulation_newcustomer')
#
#
# @login_required
# @permission_required('circulation.add_customer', raise_exception=True)
# def addAndAddNew_CustomerList(request):
#     if request.method == 'POST':
#         form = CustomerForm(request.POST)
#         if form.is_valid():
#             Customer = form.save(commit=False)
#             Customer.save()
#             return redirect_query('circulation_newcustomer')
#         else:
#             return render(request, 'circulation/customer_form.html', {'form': form})
#     return redirect('circulation_newcustomer')
#
#
# @login_required
# @permission_required('circulation.change_customer', raise_exception=True)
# def updateAndReturn_CustomerList(request, pk):
#     if request.method == 'POST':
#         client = get_object_or_404(Customer, pk=pk)
#         form = CustomerForm(request.POST, instance=client)
#         if form.is_valid():
#             Customer = form.save(commit=False)
#             Customer.save()
#             return redirect_query('circulation_newcustomer',
#                                   {'filter': Customer.identificationCode, 'search': 'identificationCode'})
#         else:
#             return render(request, 'circulation/customer_form.html', {'form': form, 'Customer': client})
#     return redirect('circulation_newcustomer')
#

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
