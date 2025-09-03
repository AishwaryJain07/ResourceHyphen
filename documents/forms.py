from django import forms
from .models import PDFDocument, CardSettings

class PDFUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings = CardSettings.get_settings()
        
        # Dynamic choices based on settings
        parent_choices = [(i, f'Parent Card {i}') for i in range(1, settings.max_parent_cards + 1)]
        subcard_choices = [(i, f'Subcard {i}') for i in range(1, settings.max_subcards + 1)]
        
        self.fields['parent_card_id'].widget = forms.Select(choices=parent_choices, attrs={'class': 'form-control'})
        self.fields['subcard_id'].widget = forms.Select(choices=subcard_choices, attrs={'class': 'form-control'})
    
    class Meta:
        model = PDFDocument
        fields = ['title', 'pdf_file', 'parent_card_id', 'subcard_id']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter document title'
            }),
            'pdf_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf'
            }),
        }
    
    def clean_pdf_file(self):
        pdf_file = self.cleaned_data.get('pdf_file')
        
        if pdf_file:
            if not pdf_file.name.lower().endswith('.pdf'):
                raise forms.ValidationError("Only PDF files are allowed.")
            
            if pdf_file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("File size cannot exceed 10MB.")
        
        return pdf_file
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title.strip()) < 3:
            raise forms.ValidationError("Title must be at least 3 characters long.")
        return title.strip()

class CardSettingsForm(forms.ModelForm):
    class Meta:
        model = CardSettings
        fields = ['max_parent_cards', 'max_subcards']
        widgets = {
            'max_parent_cards': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '50'
            }),
            'max_subcards': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '50'
            }),
        }