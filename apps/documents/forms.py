from django import forms
from django.contrib.auth.models import User
from .models import Document
from .constants import STATUS_CHOICES


class DocumentFilterForm(forms.Form):
    """
    Form for filtering documents in the document list view.
    """
    status = forms.ChoiceField(
        choices=[('', 'Статус документа')] + list(STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={
            'class': 'block rounded-md border-gray-300 text-sm focus:border-blue-500 focus:ring-blue-500'
        })
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'block rounded-md border-gray-300 text-sm focus:border-blue-500 focus:ring-blue-500',
            'placeholder': 'Пошук за номером або рахунком'
        })
    )
    asset = forms.ChoiceField(
        choices=[('', 'Актив'), ('1', 'Активний'), ('0', 'Неактивний')],
        required=False,
        widget=forms.Select(attrs={
            'class': 'block rounded-md border-gray-300 text-sm focus:border-blue-500 focus:ring-blue-500'
        })
    )
    doc_type = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'block rounded-md border-gray-300 text-sm focus:border-blue-500 focus:ring-blue-500',
            'placeholder': 'Тип'
        })
    )
    folder = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'block rounded-md border-gray-300 text-sm focus:border-blue-500 focus:ring-blue-500',
            'placeholder': 'Папка'
        })
    )
    error_code = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'block rounded-md border-gray-300 text-sm focus:border-blue-500 focus:ring-blue-500',
            'placeholder': 'Код помилки'
        })
    )
    executer = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        empty_label='Виконавець',
        widget=forms.Select(attrs={
            'class': 'block rounded-md border-gray-300 text-sm focus:border-blue-500 focus:ring-blue-500'
        })
    )
    sort_by = forms.ChoiceField(
        choices=[
            ('', 'Сортування'),
            ('-created_at', 'Спочатку новіші'),
            ('created_at', 'Спочатку старіші'),
            ('number', 'За номером (А-Я)'),
            ('-number', 'За номером (Я-А)'),
            ('date', 'За датою (↑)'),
            ('-date', 'За датою (↓)'),
        ],
        required=False,
        initial='-created_at',
        widget=forms.Select(attrs={
            'class': 'block rounded-md border-gray-300 text-sm focus:border-blue-500 focus:ring-blue-500'
        })
    )


class DocumentStatusForm(forms.Form):
    """
    Form for updating document status.
    """
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
        })
    )
    
    def clean_status(self):
        status = self.cleaned_data.get('status')
        if status not in dict(STATUS_CHOICES):
            raise forms.ValidationError("Invalid status value")
        return status 