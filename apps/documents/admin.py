"""
Admin site configuration for the documents app.
"""
from django.contrib import admin
from .models import Document, DocumentPage


class DocumentPageInline(admin.TabularInline):
    """
    Inline admin for DocumentPage, allows editing pages within Document admin.
    """
    model = DocumentPage
    extra = 1
    fields = ('page_name', 'file_path', 'discrepancy_found')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Document model.
    """
    # Display options
    list_display = (
        'number', 'contractor', 'date', 'doc_type', 
        'folder', 'status', 'executer', 'document_type', 
        'payment', 'document_owner', 'copy_original', 
        'completeness', 'created_at'
    )
    
    # Filtering options
    list_filter = (
        'status', 'folder', 'doc_type', 'executer',
        'document_type', 'copy_original', 'completeness'
    )
    
    # Search options
    search_fields = (
        'number', 'contractor', 'error_code', 
        'document_owner', 'payment'
    )
    
    # Organization options
    date_hierarchy = 'date'
    ordering = ('-created_at',)
    
    # Form organization
    fieldsets = (
        ('Основна інформація', {
            'fields': (
                'number', 'contractor', 'date', 
                'account_number', 'doc_type', 'folder', 'asset'
            )
        }),
        ('Додаткова інформація', {
            'fields': (
                'document_type', 'payment', 'document_owner', 
                'copy_original', 'completeness'
            )
        }),
        ('Статус і виконання', {
            'fields': ('status', 'error_code', 'executer')
        }),
        ('Метадані', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Read-only fields
    readonly_fields = ('created_at', 'updated_at')
    
    # Inlines
    inlines = [DocumentPageInline]


@admin.register(DocumentPage)
class DocumentPageAdmin(admin.ModelAdmin):
    """
    Admin configuration for DocumentPage model.
    """
    # Display options
    list_display = ('document', 'page_name', 'discrepancy_found', 'created_at')
    list_filter = ('discrepancy_found', 'created_at')
    search_fields = ('document__number', 'page_name')
    
    # Form organization
    fieldsets = (
        ('Основна інформація', {
            'fields': ('document', 'page_name', 'file_path', 'discrepancy_found')
        }),
        ('Метадані', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Read-only fields
    readonly_fields = ('created_at', 'updated_at')
