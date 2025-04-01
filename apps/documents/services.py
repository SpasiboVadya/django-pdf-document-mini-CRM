"""
Services for document-related operations.
Contains business logic separate from views and models.
"""
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Document


def filter_documents(queryset, filters):
    """
    Apply filters to document queryset based on form data.
    
    Args:
        queryset: Initial Document queryset
        filters: Dictionary of filter parameters
        
    Returns:
        Filtered Document queryset
    """
    # Filter by status if provided
    status = filters.get('status')
    if status:
        queryset = queryset.filter(status=status)
    
    # Filter by search query
    search_query = filters.get('search')
    if search_query:
        queryset = queryset.filter(
            Q(number__icontains=search_query) |
            Q(account_number__icontains=search_query)
        )
    
    # Filter by asset if provided
    asset = filters.get('asset')
    if asset:
        queryset = queryset.filter(asset=asset)
    
    # Filter by doc_type if provided
    doc_type = filters.get('doc_type')
    if doc_type:
        queryset = queryset.filter(doc_type=doc_type)
    
    # Filter by folder if provided
    folder = filters.get('folder')
    if folder:
        queryset = queryset.filter(folder=folder)
    
    # Filter by error_code if provided
    error_code = filters.get('error_code')
    if error_code:
        queryset = queryset.filter(error_code=error_code)
    
    # Filter by executer if provided
    executer = filters.get('executer')
    if executer:
        queryset = queryset.filter(executer_id=executer)
    
    # Sort by parameter if provided
    sort_by = filters.get('sort_by', '-created_at')
    if sort_by and sort_by.strip():  # Check if sort_by is not empty
        queryset = queryset.order_by(sort_by)
    else:
        # Default ordering if sort_by is empty
        queryset = queryset.order_by('-created_at')
    
    return queryset


def get_document_filter_options():
    """
    Get unique values for document filter dropdowns.
    
    Returns:
        Dictionary with filter options
    """
    return {
        'asset_values': Document.objects.exclude(asset__isnull=True)
                                .values_list('asset', flat=True)
                                .distinct(),
        'folder_values': Document.objects.exclude(folder__exact='')
                                 .values_list('folder', flat=True)
                                 .distinct(),
        'error_code_values': Document.objects.exclude(error_code__isnull=True)
                                      .exclude(error_code__exact='')
                                      .values_list('error_code', flat=True)
                                      .distinct(),
        'doc_type_values': Document.objects.exclude(doc_type__exact='')
                                   .values_list('doc_type', flat=True)
                                   .distinct(),
        'executer_values': User.objects.all(),
        'update_time': datetime.now().strftime('%d.%m.%Y о %H:%M'),
    }


def get_document_counts():
    """
    Get document counts by status for dashboard display.
    
    Returns:
        Dictionary with counts by status
    """
    return {
        'total_count': Document.objects.count(),
        'queue_count': Document.objects.filter(status='queue').count(),
        'in_progress_count': Document.objects.filter(status='in_progress').count(),
        'completed_count': Document.objects.filter(status='completed').count(),
    }


def update_document_status(document_id, new_status):
    """
    Update a document's status.
    
    Args:
        document_id: ID of the document to update
        new_status: New status value
        
    Returns:
        Tuple of (success, error_message)
    """
    try:
        document = Document.objects.get(pk=document_id)
        document.status = new_status
        document.save()
        return True, None
    except Document.DoesNotExist:
        return False, "Document not found"
    except Exception as e:
        return False, str(e) 