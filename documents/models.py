from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import os

def pdf_upload_path(instance, filename):
    return f'pdf_docs/parent_{instance.parent_card_id}/sub_{instance.subcard_id}/{filename}'

class PDFDocument(models.Model):
    title = models.CharField(max_length=200, help_text="Title of the PDF document")
    pdf_file = models.FileField(
        upload_to=pdf_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="Upload PDF file only"
    )
    uploaded_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        help_text="User who uploaded this document"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    parent_card_id = models.CharField(
        max_length=100,
        help_text="Parent card number"
    )
    subcard_id = models.CharField(
        max_length=100,
        help_text="Subcard number"
    )

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "PDF Document"
        verbose_name_plural = "PDF Documents"
    
    def __str__(self):
        return f"{self.title} (P{self.parent_card_id}.{self.subcard_id})"
    
    def get_file_size(self):
        if self.pdf_file:
            size = self.pdf_file.size
            if size < 1024:
                return f"{size} B"
            elif size < 1024 * 1024:
                return f"{size / 1024:.1f} KB"
            else:
                return f"{size / (1024 * 1024):.1f} MB"
        return "Unknown"
    
    def get_filename(self):
        if self.pdf_file:
            return os.path.basename(self.pdf_file.name)
        return "No file"
    
    def delete(self, *args, **kwargs):
        if self.pdf_file:
            if os.path.isfile(self.pdf_file.path):
                os.remove(self.pdf_file.path)
        super().delete(*args, **kwargs)

class CardSettings(models.Model):
    max_parent_cards = models.CharField(max_length=100, default='10')
    max_subcards = models.CharField(max_length=100, default='10')
    
    class Meta:
        verbose_name = "Card Settings"
        verbose_name_plural = "Card Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and CardSettings.objects.exists():
            raise ValueError("Only one CardSettings instance allowed")
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        settings, created = cls.objects.get_or_create(defaults={'max_parent_cards': 10, 'max_subcards': 10})
        return settings