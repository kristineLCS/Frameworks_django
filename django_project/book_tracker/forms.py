from django import forms

class BookSearchForm(forms.Form):
    query = forms.CharField(label='Search Books', max_length=100, required=True)
