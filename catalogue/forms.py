from django import forms
from catalogue.models import (BoardGameItem, RentalClient)

class BoardGameForm(forms.ModelForm):

    class Meta():
        model = BoardGameItem
        fields = ('codeValue', 'itemLabel', 'bggURL')

        labels = {
            'itemLabel' : 'Tytuł',
            'codeValue' : 'Kod paskowy',
            'bggURL' : 'BGG link',
        }

        widgets = {
            'itemLabel': forms.TextInput(attrs={'class':'textinputclass',
                'placeholder':'Wprowadź tytuł'}),
            'codeValue': forms.TextInput(attrs={'class':'textinputclass',
                'placeholder':'Wczytaj kod paskowy'}),
            'bggURL': forms.URLInput(attrs={'class':'urlinputclass',
                'placeholder':'Podaj adres strony gry w serwisie boardgamegeek.com'})
        }


class RentalClientForm(forms.ModelForm):

    class Meta():
        model = RentalClient
        fields = ('identificationCode', 'initials')

        labels = {
            'identificationCode' : 'Oznaczenie Identyfikacyjne',
            'initials' : 'Inicjały',
        }

        placeholders = {
            'identificationCode' : 'Wprowadź oznaczenie identyfikacyjne',
            'initials' : 'Wprowadź inicjały',
        }

        widgets = {
            'itemLabel': forms.TextInput(attrs={'class':'textinputclass'}),
            'codeValue': forms.TextInput(attrs={'class':'textinputclass'})
        }