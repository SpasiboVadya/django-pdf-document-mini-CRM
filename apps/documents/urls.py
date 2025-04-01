"""
URL patterns for the documents app.
"""
from django.urls import path
from .views import DocumentListView, DocumentDetailView, update_document_status

app_name = 'documents'

urlpatterns = [
    # Document list view - Main entry point for the app
    path('', 
         DocumentListView.as_view(), 
         name='document_list'),
    
    # Document detail view - Shows a single document with its pages
    path('<int:pk>/', 
         DocumentDetailView.as_view(), 
         name='document_detail'),
    
    # AJAX endpoint for updating document status
    path('<int:pk>/update-status/', 
         update_document_status, 
         name='update_document_status'),
] 