from django.contrib import admin
from .models import Document, DocumentPage

class DocumentPageInline(admin.TabularInline):
    model = DocumentPage
    extra = 1

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('number', 'contractor', 'date', 'doc_type', 'folder', 'status', 'executer', 'document_type', 'payment', 'document_owner', 'copy_original', 'completeness', 'created_at')
    list_filter = ('status', 'folder', 'doc_type', 'executer', 'document_type', 'copy_original', 'completeness')
    search_fields = ('number', 'contractor', 'error_code', 'document_owner', 'payment')
    date_hierarchy = 'date'
    ordering = ('-created_at',)
    fieldsets = (
        ('Основна інформація', {
            'fields': ('number', 'contractor', 'date', 'account_number', 'doc_type', 'folder', 'asset')
        }),
        ('Додаткова інформація', {
            'fields': ('document_type', 'payment', 'document_owner', 'copy_original', 'completeness')
        }),
        ('Статус і виконання', {
            'fields': ('status', 'error_code', 'executer')
        }),
    )
    inlines = [DocumentPageInline]

@admin.register(DocumentPage)
class DocumentPageAdmin(admin.ModelAdmin):
    list_display = ('document', 'page_name', 'discrepancy_found')
    list_filter = ('discrepancy_found',)
    search_fields = ('document__number', 'page_name')
