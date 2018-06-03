from django import forms
from django.core.exceptions import ValidationError
from dal import autocomplete

from circulation.models import RentalClient, ClientID, BoardGameLending

class RentalClientForm(forms.ModelForm):
    class Meta:
        model = RentalClient
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

class RentalClientIDInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        cleaned = super(RentalClientIDInlineFormSet, self).clean()
        numOfActiveIDs = 0;
        for form in self.forms:
            if form.cleaned_data.get('active'):
                numOfActiveIDs+=1;
        if numOfActiveIDs > 1:
            raise forms.ValidationError('Tylko jeden identyfikator może być aktywny')

        return cleaned

class BoardGameLendingForm(forms.ModelForm):
    class Meta:
        model = BoardGameLending

        fields = ('client', 'container')

        labels = {'client': 'Dla klienta',
                  'container': 'Kontener',
        }

        widgets = {
            'client': autocomplete.ModelSelect2(
                url='clientbyidlabel-autocomplete',
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

        client = cleaned.get('client')
        # if client.BoardGameLending.objects.filter(returned=None).count() > 0:
        #     raise ValidationError('użytkownik wypożyczył już grę')

        return cleaned
