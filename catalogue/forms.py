from django import forms
from catalogue.models import BoardGameItem, BoardGameCommodity

class BoardGameItemForm(forms.ModelForm):

    class Meta():
        model = BoardGameItem
        # extensions =

        fields = ('baseGameItem', 'itemLabel', 'bggURL')

        labels = {
            'itemLabel' : 'Tytuł',
            'bggURL' : 'BGG link',
            'baseGameItem' : "Gra podstawowa"
        }

        widgets = {
            'itemLabel': forms.TextInput(attrs={'class':'textinputclass',
                'placeholder':'Wprowadź tytuł'}),
            'bggURL': forms.URLInput(attrs={'class':'urlinputclass',
                'placeholder':'Podaj adres strony gry w serwisie boardgamegeek.com'}),
            'baseGameItem': forms.Select(attrs={'class': 'selectclass',
                'empty_label' : "Dla dodatku wskaż podstawową grę"}),
        }


class BoardGameCommodityForm(forms.ModelForm):

    # def __init__ (self, *args, **kwargs):
    #     super.__init__(*args, **kwargs)

    class Meta():
        model = BoardGameCommodity
        # extensions =

        fields = ('catalogueEntry', 'codeValue', 'boxFrontImage', 'boxTopImage', 'boxSideImage')

        labels = {
            'catalogueEntry' : 'Tytuł katalogowy',
            'codeValue' : 'Kod paskowy',
            'boxFrontImage' : 'Przód',
            'boxSideImage' : "Bok",
            'boxTopImage' : "Wierzch"
        }


        widgets = {
            'codeValue': forms.TextInput(attrs={'class':'textinputclass',
                'placeholder':'Wczytaj kod paskowy'}),
        }