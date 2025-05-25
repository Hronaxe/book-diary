from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from core.models import Book, Author, Genre


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ['uploaded_by']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Сохранить'))

        for field_name in ['author', 'genre']:
            model = self.fields[field_name].queryset.model
            add_url = f"/profile/add_" + field_name + "_popup"
            self.fields[field_name].widget.attrs.update({
                'data-popup-url': add_url,
                'class': 'foreign-key-popup-select'
            })

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']


