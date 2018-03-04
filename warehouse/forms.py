from django import forms

from warehouse.models import Warehouse, BoardGameContainer


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ('name', 'desc')
        labels = {'name': 'nazwa', 'desc': 'opis'}
        placeholders = {'name': 'dodaj nazwę', 'desc': ''}
        widgets = {'name': forms.TextInput(attrs={'class': 'textinputclass'}),
                   'desc': forms.Textarea()}


class BoardGameContainerForm(forms.ModelForm):
    class Meta:
        model = BoardGameContainer
        fields = ('warehouse', 'commodity', 'total')
        labels = {'warehouse': 'magazyn',
                  'commodity': 'tytuł',
                  'total': 'liczba egzemplarzy'}
