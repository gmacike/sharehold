from django import forms
from dal import autocomplete

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

    def __init__ (self, *args, **kwargs):
        initVals = kwargs.get('initial', {})
        commodity = initVals.pop ('commodity', None)
        if commodity == None:
            initVals['total'] = 1
            kwargs['initial'] = initVals
        super(BoardGameContainerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = BoardGameContainer

        fields = ('warehouse', 'commodity', 'total')

        labels = {'warehouse': 'Magazyn',
                  'commodity': 'Przedmiot',
                  'total': 'Liczba egzemplarzy',
        }

        widgets = {
            'warehouse': autocomplete.ModelSelect2(
                url='warehouse-autocomplete',
                attrs={'data-placeholder': 'Wpisz nazwę magazynu...',
                    'data-minimum-input-length': 1,}
                ),

            'commodity': autocomplete.ModelSelect2(
                url='commodity-notinwarehouse-autocomplete',
                attrs={'data-placeholder': 'Wpisz kod przedmiotu...',
                    'data-minimum-input-length': 1,}
                ),

            'total': forms.NumberInput(attrs={'class': 'numberinputclass',
                                            'placeholder': 'Podaj liczbę egzemplarzy'}),
        }

        initials = {
            'total': 1,
        }
