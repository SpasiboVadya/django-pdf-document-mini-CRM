from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Document, DocumentPage
from datetime import datetime

class DocumentListView(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'documents/document_list.html'
    context_object_name = 'documents'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by status if provided
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        # Filter by search query
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(number__icontains=search_query) |
                Q(account_number__icontains=search_query)
            )
            
        # Filter by asset if provided
        asset = self.request.GET.get('asset')
        if asset:
            queryset = queryset.filter(asset=asset)
            
        # Filter by doc_type if provided
        doc_type = self.request.GET.get('doc_type')
        if doc_type:
            queryset = queryset.filter(doc_type=doc_type)
            
        # Filter by folder if provided
        folder = self.request.GET.get('folder')
        if folder:
            queryset = queryset.filter(folder=folder)
            
        # Filter by error_code if provided
        error_code = self.request.GET.get('error_code')
        if error_code:
            queryset = queryset.filter(error_code=error_code)
            
        # Filter by executer if provided
        executer = self.request.GET.get('executer')
        if executer:
            queryset = queryset.filter(executer_id=executer)
            
        # Sort by parameter if provided
        sort_by = self.request.GET.get('sort_by', '-created_at')
        queryset = queryset.order_by(sort_by)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get distinct values for filters
        context['asset_values'] = Document.objects.exclude(asset__isnull=True).values_list('asset', flat=True).distinct()
        context['folder_values'] = Document.objects.exclude(folder__exact='').values_list('folder', flat=True).distinct()
        context['error_code_values'] = Document.objects.exclude(error_code__isnull=True).exclude(error_code__exact='').values_list('error_code', flat=True).distinct()
        context['doc_type_values'] = Document.objects.exclude(doc_type__exact='').values_list('doc_type', flat=True).distinct()
        context['executer_values'] = User.objects.all()
        
        # Add update time
        context['update_time'] = datetime.now().strftime('%d.%m.%Y о %H:%M')
        
        return context


class DocumentDetailView(LoginRequiredMixin, DetailView):
    model = Document
    template_name = 'documents/document_detail.html'
    context_object_name = 'document'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pages'] = self.object.pages.all()
        return context


@login_required
def update_document_status(request, pk):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        document = get_object_or_404(Document, pk=pk)
        new_status = request.POST.get('status')
        
        if new_status and new_status in dict(Document.STATUS_CHOICES):
            document.status = new_status
            document.save()
            return JsonResponse({'success': True})
            
    return JsonResponse({'success': False}, status=400)
