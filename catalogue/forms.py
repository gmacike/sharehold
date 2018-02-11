from django import forms
from catalogue.models import BoardGameItem

class BoardGameForm(forms.ModelForm):

    class Meta():
        model = BoardGameItem
        fields = ('codeValue', 'itemLabel', 'bggURL')

        widgets = {
            'Tytuł': forms.TextInput(attrs={'class':'textinputclass'}),
            'Kod': forms.TextInput(attrs={'class':'textinputclass'}),
            'Strona BGG': forms.URLInput(attrs={'class':'urlinputclass'})
        }
