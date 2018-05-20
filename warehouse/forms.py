from django import forms

from warehouse.models import Warehouse, BoardGameContainer


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ('name', 'desc')
        labels = {'name': 'Nazwa magazynu', 'desc': 'Opis magazynu'}
        placeholders = {'name': 'dodaj nazwę', 'desc': ''}
        widgets = {'name': forms.TextInput({'class': 'textinputclass'}),
                   'desc': forms.Textarea()}


class BoardGameContainerForm(forms.ModelForm):
    class Meta:
        model = BoardGameContainer
        fields = ('warehouse', 'commodity', 'total')
        labels = {'warehouse': 'Magazyn',
                  'commodity': 'Przedmiot',
                  'total': 'Liczba egzemplarzy'}
