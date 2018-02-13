from django import forms
from catalogue.models import BoardGameItem

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
