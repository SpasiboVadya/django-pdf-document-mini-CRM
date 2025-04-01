from django.contrib import admin
from .models import Document, DocumentPage

class DocumentPageInline(admin.TabularInline):
    model = DocumentPage
    extra = 1

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('number', 'contractor', 'date', 'doc_type', 'folder', 'status', 'executer', 'created_at')
    list_filter = ('status', 'folder', 'doc_type', 'executer')
    search_fields = ('number', 'contractor', 'error_code')
    date_hierarchy = 'date'
    ordering = ('-created_at',)
    inlines = [DocumentPageInline]

@admin.register(DocumentPage)
class DocumentPageAdmin(admin.ModelAdmin):
    list_display = ('document', 'page_name', 'discrepancy_found', 'copy_original', 'completeness')
    list_filter = ('discrepancy_found', 'copy_original', 'completeness')
    search_fields = ('document__number', 'page_name')
