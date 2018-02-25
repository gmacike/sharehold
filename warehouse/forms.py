from django import forms

from warehouse.models import Warehouse, Container


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
