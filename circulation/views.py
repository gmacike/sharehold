from urllib.parse import urlencode

from datetime import datetime
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from dal import autocomplete
from django.forms import inlineformset_factory
from circulation.models import (Customer, CustomerID, BoardGameLending)
from warehouse.models import Warehouse, BoardGameContainer
from circulation.forms import (CustomerForm, BoardGameLendingForm)
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
    if request.user.has_perm ('circulation.add_customerid'):
        return redirect('circulation_addcustomerid')
    if request.user.has_perm('circulation.change_customerid'):
        # TODO implement view for changing idstatus only
        pass
    return redirect('circulation_newcustomer')


############################################
# customer Views
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


@login_required
@has_any_permission (('circulation.add_customerid', 'circulation.change_customerid',
    'circulation.add_customer', 'circulation.change_customer'))
def get_customer_by_IDlabel (request):
    customers = Customer.objects.none()
    custpk = None
    if request.method == 'GET':
        if request.GET.__contains__("filter"):
            filter_criteria = request.GET.get("filter")
            # self.request.session ['catalogue_filter'] = filter_criteria
            # else:
            #     filter_criteria = self.request.session.get ('catalogue_filter', None)
            if filter_criteria != None:
                # expected one and only one Customer matching the criteria
                # TODO zrefaktoryzować, bo można jakoś inteligentniej poprzez get()
                customers = Customer.objects.filter(CustomerIDs__IDlabel__iexact=filter_criteria)
                if customers.count() == 1:
                    custpk = customers[0].pk
        if custpk == None:
            return redirect('circulation_newcustomer')
    return redirect('circulation_customeredit', pk = custpk)

class CustomerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'circulation.change_customer'
    raise_exception = True

    form_class = CustomerForm
    model = Customer

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance = Customer.objects.get(pk=kwargs['pk']))
        if form.is_valid():
            try:
                cust = form.save(commit=False)
                newID = form.cleaned_data['newCustomerID']
                if newID != "":
                    # create activates ID
                    custID = CustomerID.create (cust, newID)
                    custID.save()
                cust.save()
            except ValidationError as exc:
                form.add_error('newCustomerID', exc)
                return render(request, 'circulation/customer_form.html', {'form': form, 'customer': self.get_object,})
        else:
            # dupa=form.errors
            # dupa.blada
            return render(request, 'circulation/customer_form.html', {'form': form, 'customer': self.get_object,})
        return redirect(cust)


class CustomerAutocompleteViewByActiveIDlabel(LoginRequiredMixin, PermissionRequiredMixin, autocomplete.Select2QuerySetView):
    permission_required = 'circulation.add_boardgamelending'
    raise_exception = True

    def get_queryset(self):
        qs = Customer.objects.all().exclude(CustomerIDs__IDstatus!=CustomerID.AKTYWNY).order_by('CustomerIDs__IDlabel')
        if self.q:
            qs = qs.filter(CustomerIDs__IDlabel__icontains=self.q)
        return qs



class CustomerAutocompleteViewByIDlabel(LoginRequiredMixin, PermissionRequiredMixin, autocomplete.Select2QuerySetView):
    permission_required = 'circulation.change_customer'
    raise_exception = True

    def get_queryset(self):
        qs = Customer.objects.all().order_by('CustomerIDs__IDlabel')
        if self.q:
            qs = qs.filter(CustomerIDs__IDlabel__icontains=self.q)
        return qs

@login_required
@permission_required ('circulation.change_customerid', raise_exception=True)
def CustomerID_activate (request, IDpk):
    try:
        custID = CustomerID.objects.get(pk=IDpk)
        custID.activate()
        # if no ValidationError raised
        custID.save()
    except CustomerID.DoesNotExist as exc:
        pass
    except ValidationError as exc:
        messages.info(request, 'Identyfikator nie może być aktywowany')
    return redirect('circulation_customeredit', pk = custID.customer.pk)

@login_required
@permission_required ('circulation.change_customerid', raise_exception=True)
def customerID_deactivate (request, IDpk):
    try:
        custID = CustomerID.objects.get(pk=IDpk)
        custID.deactivate()
        # if no ValidationError raised
        custID.save()
    except CustomerID.DoesNotExist as exc:
        pass
    except ValidationError as exc:
        messages.info(request, 'Identyfikator nie może być zablokowany')
    return redirect('circulation_customeredit', pk = custID.customer.pk)

#
# class BoardGameUpdate2View(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
#     permission_required = 'circulation.change_customer'
#     raise_exception = True
#
#     form_class = CustomerForm
#     model = Customer

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
            cust = form.save()
            custID = CustomerID.objects.create (customer=cust, IDlabel=form.cleaned_data['newCustomerID'])
            custID.activate()
            # TODO: zarejestrować kto i kiedy
            # customer.save()
            custID.save()
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
#         customer = get_object_or_404(Customer, pk=pk)
#         form = CustomerForm(request.POST, instance=client)
#         if form.is_valid():
#             Customer = form.save(commit=False)
#             Customer.save()
#             return redirect_query('circulation_newcustomer',
#                                   {'filter': Customer.identificationCode, 'search': 'identificationCode'})
#         else:
#             return render(request, 'circulation/customer_form.html', {'form': form, 'Customer': customer})
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
