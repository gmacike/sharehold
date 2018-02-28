from django import forms
from circulation.models import RentalClient

class RentalClientForm(forms.ModelForm):

    class Meta():
        model = RentalClient
        fields = ('identificationCode', 'initials')

        labels = {
            'identificationCode' : 'Oznaczenie Identyfikacyjne',
            'initials' : 'Inicjały',
        }

        widgets = {
            'identificationCode': forms.TextInput(attrs={'class':'textinputclass', 'placeholder' : 'Wprowadź oznaczenie identyfikacyjne'}),
            'initials': forms.TextInput(attrs={'class':'textinputclass', 'placeholder' : 'Wprowadź inicjały'})
        }
		