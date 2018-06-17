from django import forms
from django.core.exceptions import ValidationError
from dal import autocomplete

from circulation.models import Customer, CustomerID, BoardGameLending

class CustomerForm(forms.ModelForm):
    newCustomerID = forms.CharField(max_length=12, required=False, label='Nowy identyfikator dla klienta',
        widget=forms.TextInput(attrs={'placeholder': 'Podaj numer nowego identyfikatora wydawanego klientowi'}))

    class Meta:
        model = Customer
        fields = ('registrationNumber', 'initials')

        labels = {
            'registrationNumber': 'Zarejestrowany jako',
            'initials': 'Inicjały',
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

# class RentalCustomerIDInlineFormSet(forms.BaseInlineFormSet):
#     def clean(self):
#         cleaned = super(RentalCustomerIDInlineFormSet, self).clean()
#         numOfActiveIDs = 0;
#         for form in self.forms:
#             if form.cleaned_data.get('active'):
#                 numOfActiveIDs+=1;
#         if numOfActiveIDs > 1:
#             raise forms.ValidationError('Tylko jeden identyfikator może być aktywny')
#
#         return cleaned

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
                attrs={'data-placeholder': 'Podaj identyfikator klienta...',
                    'data-minimum-input-length': 3,}
                ),

            'container': autocomplete.ModelSelect2(
                url='containerbycommodity-autocomplete',
                attrs={'data-placeholder': 'Wpisz kod przedmiotu...',
                    'data-minimum-input-length': 1,}
                ),

        }


    def clean(self):
        cleaned = super().clean()
        container = cleaned.get('container')
        if container.available <= 0:
            raise ValidationError('brak dostępnych egzemplarzy w magazynie')

        customer = cleaned.get('customer')
        # if customer.BoardGameLending.objects.filter(returned=None).count() > 0:
        #     raise ValidationError('użytkownik wypożyczył już grę')

        return cleaned
