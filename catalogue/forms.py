from django import forms
from dal import autocomplete
# from django.forms import inlineformset_factory
from catalogue.models import BoardGameItem, BoardGameCommodity


class BoardGameItemForm(forms.ModelForm):

    class Meta():
        model = BoardGameItem

        fields = ('itemLabel', 'itemImage', 'bggURL', 'baseGameItem')

        labels = {
            'itemLabel': 'Tytuł',
            'itemImage': 'Zdjęcie pudełka',
            'bggURL': 'BGG link',
            'baseGameItem': "Gra podstawowa"
        }

        widgets = {
            'itemLabel': forms.TextInput(attrs={'class': 'textinputclass',
                                                'placeholder': 'Wprowadź tytuł',
                                                'autofocus': True,}),
            'bggURL': forms.URLInput(attrs={'class': 'urlinputclass',
                                            'placeholder': 'Podaj adres strony gry w serwisie boardgamegeek.com'}),
            'baseGameItem': autocomplete.ModelSelect2(
                url='boardgame-autocomplete',
                attrs={'data-placeholder': 'Wpisz tytuł gry podstawowej...',
                    'data-minimum-input-length': 1,}
                ),
        }

# BoardGameItemFormSet = inlineformset_factory (BoardGameItem, BoardGameItem, form = BoardGameItemForm, extra = 1)


class BoardGameCommodityForm(forms.ModelForm):

    class Meta():
        model = BoardGameCommodity
        # extensions =

        fields = ('catalogueEntry', 'codeValue', 'description',
            'boxFrontImage', 'boxTopImage', 'boxSideImage')

        labels = {
            'catalogueEntry': 'Tytuł katalogowy',
            'codeValue': 'Kod paskowy',
            'boxFrontImage': 'Przód',
            'boxSideImage': "Bok",
            'boxTopImage': "Wierzch"
        }

        widgets = {
            'codeValue': forms.TextInput(attrs={'class': 'textinputclass',
                                                'placeholder': 'Wczytaj kod paskowy',
                                                'autofocus': True,}),
            'catalogueEntry': autocomplete.ModelSelect2(
                url='boardgame-autocomplete',
                attrs={'data-placeholder': 'Wpisz tytuł gry...',
                    'data-minimum-input-length': 1,}
                ),
        }
