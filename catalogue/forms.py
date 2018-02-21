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

        widgets = {
            'itemLabel': forms.TextInput(attrs={'class':'textinputclass',
                'placeholder':'Wprowadź tytuł'}),
            'codeValue': forms.TextInput(attrs={'class':'textinputclass',
                'placeholder':'Wczytaj kod paskowy'}),
            'bggURL': forms.URLInput(attrs={'class':'urlinputclass',
                'placeholder':'Podaj adres strony gry w serwisie boardgamegeek.com'})
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
