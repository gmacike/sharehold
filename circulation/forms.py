from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings
from dal import autocomplete

from circulation.models import Customer, CustomerID, BoardGameLending

class CustomerForm(forms.ModelForm):
    newCustomerID = forms.CharField(max_length=12, required=False, label='Nowy identyfikator dla klienta',
        widget=forms.TextInput(attrs={'placeholder': 'Podaj numer nowego identyfikatora wydawanego klientowi'}))

    class Meta:
        model = Customer
        fields = ('registrationNumber', 'nick')

        labels = {
            'registrationNumber': 'Zarejestrowany jako',
            'nick': 'Pseudonim',
        }

        widgets = {
            'registrationNumber': forms.TextInput({
                'class': 'textinputclass',
                'placeholder': 'Wprowadź oznaczenie identyfikacyjne'
            }),
            'initials': forms.TextInput({
                'class': 'textinputclass',
                'placeholder': 'Wprowadź inicjały'
            })
        }


    def clean_newCustomerID(self):
        # cleaned = super(CustomerForm, self).clean()
        newID = self.cleaned_data['newCustomerID']
        if self.instance.pk == None and newID == "":
            raise forms.ValidationError ('Dla nowego klienta podanie identyfikatora jest obowiązkowe', code='missing required data')
        if newID != "" and CustomerID.objects.filter(IDlabel__iexact=newID).exists():
            raise forms.ValidationError ('Podany identyfikator został już zarejestrowany', code='duplicated unique data')
        return newID

class BoardGameLendingForm(forms.ModelForm):
    class Meta:
        model = BoardGameLending

        fields = ('customer', 'container')

        labels = {'customer': 'Dla klienta',
                  'container': 'Kontener',
        }

        widgets = {
            'customer': autocomplete.ModelSelect2(
                url='customerbyactiveidlabel-autocomplete',
                attrs={'data-placeholder': 'Podaj aktywny identyfikator klienta...',
                    'data-minimum-input-length': 3,}
                ),

            'container': autocomplete.ModelSelect2(
                url='containerbycommodity-autocomplete',
                attrs={'data-placeholder': 'Wpisz kod przedmiotu...',
                    'data-minimum-input-length': 3,}
                ),

        }


    def clean_customer(self):
        # cleaned = super(CustomerForm, self).clean()
        cust = self.cleaned_data['customer']
        if cust.get_unfinished_lendings_count() >= settings.CIRCULATION_MAX_LENDINGS_PER_CUSTOMER:
            raise ValidationError ('Klient wyczerpał limit wypożyczeń')
        return cust

    def clean_container(self):
        container = self.cleaned_data['container']
        if container.available <= 0:
            raise ValidationError('Brak dostępnych egzemplarzy w magazynie')
        return container

class BoardGameReturnForm(forms.ModelForm):
    class Meta:
        model = BoardGameLending

        fields = ('customer', 'container')

        labels = {'customer': 'Klient',
                  'container': 'Wypożyczony przedmiot',
        }

        widgets = {
            'customer': autocomplete.ModelSelect2(
                url='returncustomerbynickorcustid-autocomplete',
                attrs={'data-placeholder': 'Podaj pseudonim albo identyfikator klienta...',
                    'data-minimum-input-length': 3,},
                forward=('container',)
                ),

            'container': autocomplete.ModelSelect2(
                url='containerbyunfinishedlendings-autocomplete',
                attrs={'data-placeholder': 'Wpisz kod lub tytuł katalogowy przedmiotu...',
                    'data-minimum-input-length': 3,},
                forward=('customer',)
                ),

        }
