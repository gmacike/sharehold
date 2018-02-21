from django import forms
from catalogue.models import BoardGameItem, Warehouse, Container


class BoardGameForm(forms.ModelForm):

    class Meta():
        model = BoardGameItem
        fields = ('codeValue', 'itemLabel', 'bggURL')

        labels = {
            'itemLabel' : 'Tytuł',
            'codeValue' : 'Kod paskowy',
            'bggURL' : 'BGG link',
        }

        placeholders = {
            'itemLabel' : 'Wprowadź tytuł',
            'codeValue' : 'Wczytaj kod paskowy',
            'bggURL' : 'Podaj adres strony gry w serwisie boardgamegeek.com',
        }

        widgets = {
            'itemLabel': forms.TextInput(attrs={'class':'textinputclass'}),
            'codeValue': forms.TextInput(attrs={'class':'textinputclass'}),
            'bggURL': forms.URLInput(attrs={'class':'urlinputclass'})
        }


class WarehouseForm(forms.ModelForm):
    class Meta():
        model = Warehouse
        fields = ('name', 'desc')
        labels = {'name': 'nazwa', 'desc': 'opis'}
        placeholders = {'name': 'dodaj nazwę', 'desc': ''}
        widgets = {'name': forms.TextInput(attrs={'class': 'textinputclass'}),
                   'desc': forms.Textarea()}


class ContainerForm(forms.ModelForm):
    class Meta:
        model = Container
        fields = ('warehouse', 'board_game', 'total')
