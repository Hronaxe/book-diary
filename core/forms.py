from django import forms
from .models import ReadingDiaryEntry, Quote, Note

RATING_WIDGET = forms.NumberInput(attrs={'min': 1, 'max': 5, 'type': 'number'})

class ReadingDiaryEntryForm(forms.ModelForm):
    class Meta:
        model = ReadingDiaryEntry
        fields = [
            'emotions_rating', 'plot_originality', 'character_development',
            'world_building', 'romance', 'humor', 'meaning',
        ]
        widgets = {
            'emotions_rating': RATING_WIDGET,
            'plot_originality': RATING_WIDGET,
            'character_development': RATING_WIDGET,
            'world_building': RATING_WIDGET,
            'romance': RATING_WIDGET,
            'humor': RATING_WIDGET,
            'meaning': RATING_WIDGET,
            #'summary': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'emotions_rating': 'Эмоции',
            'plot_originality': 'Оригинальность сюжета',
            'character_development': 'Развитие персонажей',
            'world_building': 'Мир',
            'romance': 'Романтика',
            'humor': 'Юмор',
            'meaning': 'Смысл',
            #'summary': 'Резюме',
        }

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['page', 'text']
        labels = {
            'page': 'Страница',
            'text': 'Цитата',
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['page', 'text']
        labels = {
            'page': 'Страница',
            'text': 'Заметка',
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }

