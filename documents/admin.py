from django.contrib import admin
from .models import PDFDocument

@admin.register(PDFDocument)
class PDFDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent_card_id', 'subcard_id', 'uploaded_by', 'uploaded_at', 'get_file_size']
    list_filter = ['parent_card_id', 'subcard_id', 'uploaded_at', 'uploaded_by']
    search_fields = ['title', 'uploaded_by__email']
    readonly_fields = ['uploaded_at', 'get_file_size']
    
    def get_file_size(self, obj):
        return obj.get_file_size()
    get_file_size.short_description = 'File Size'