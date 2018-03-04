from django import forms
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


class ClientHasBoardGameForm(forms.ModelForm):
    class Meta:
        model = ClientHasBoardGame
        fields = ('client', 'container')
