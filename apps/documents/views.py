"""
Views for the documents app.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Document, DocumentPage
from datetime import datetime
from django.views.decorators.http import require_http_methods

from .forms import DocumentFilterForm, DocumentStatusForm
from .services import (
    filter_documents,
    get_document_filter_options,
    get_document_counts,
    update_document_status as update_doc_status
)
from .constants import ITEMS_PER_PAGE


class DocumentListView(LoginRequiredMixin, ListView):
    """
    Display a paginated list of documents with filtering options.
    """
    model = Document
    template_name = 'documents/document_list.html'
    context_object_name = 'documents'
    paginate_by = ITEMS_PER_PAGE
    
    def get_queryset(self):
        """Apply filters from form data to the queryset."""
        queryset = super().get_queryset()
        
        # Create filter form with request data
        self.filter_form = DocumentFilterForm(self.request.GET)
        
        # Apply filters if form is valid
        if self.filter_form.is_valid():
            return filter_documents(queryset, self.filter_form.cleaned_data)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Add filter options and document counts to context."""
        context = super().get_context_data(**kwargs)
        
        # Add filter form to context
        context['filter_form'] = self.filter_form
        
        # Add filter options
        context.update(get_document_filter_options())
        
        # Add document counts
        context.update(get_document_counts())
        
        return context


class DocumentDetailView(LoginRequiredMixin, DetailView):
    """
    Display detailed information about a document and its pages.
    """
    model = Document
    template_name = 'documents/document_detail.html'
    context_object_name = 'document'
    
    def get_context_data(self, **kwargs):
        """Add page information and PDF viewer data to context."""
        context = super().get_context_data(**kwargs)
        
        # Get document pages with prefetch for better performance
        pages = self.object.pages.all()
        context['pages'] = pages
        
        # Check if any pages have discrepancies
        context['has_discrepancy'] = pages.filter(discrepancy_found=True).exists()
        
        # Find the first PDF file for the document viewer
        first_pdf = pages.filter(file_path__endswith='.pdf').first()
        context['first_pdf'] = first_pdf
        
        # Add status form for updating document status
        context['status_form'] = DocumentStatusForm(initial={'status': self.object.status})
        
        return context


@login_required
@require_http_methods(["POST"])
def update_document_status(request, pk):
    """
    Update the status of a document via AJAX.
    """
    form = DocumentStatusForm(request.POST)
    
    if form.is_valid():
        success, error = update_doc_status(pk, form.cleaned_data['status'])
        
        if success:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': error}, status=404 if error == "Document not found" else 500)
    
    return JsonResponse({'success': False, 'error': form.errors['status'][0]}, status=400)
