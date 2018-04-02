from django import forms
from django.core.exceptions import ValidationError

from circulation.models import RentalClient, ClientHasBoardGame


class RentalClientForm(forms.ModelForm):
    class Meta:
        model = RentalClient
        fields = ('identificationCode', 'initials')

        labels = {
            'identificationCode': 'Oznaczenie Identyfikacyjne',
            'initials': 'Inicjały',
        }

        widgets = {
            'identificationCode': forms.TextInput({
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

class ClientHasBoardGameForm(forms.ModelForm):
    class Meta:
        model = ClientHasBoardGame
        fields = ('client', 'container')

    def clean(self):
        cleaned = super().clean()
        container = cleaned.get('container')
        if container.available <= 0:
            raise ValidationError('brak dostępnych egzemplarzy w magazynie')

        client = cleaned.get('client')
        if client.clienthasboardgame_set.filter(returned=None).count() > 0:
            raise ValidationError('użytkownik wypożyczył już grę')

        return cleaned
