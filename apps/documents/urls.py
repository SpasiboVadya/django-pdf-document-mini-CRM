from django.urls import path
from .views import DocumentListView, DocumentDetailView, update_document_status

app_name = 'documents'

urlpatterns = [
    path('', DocumentListView.as_view(), name='document_list'),
    path('<int:pk>/', DocumentDetailView.as_view(), name='document_detail'),
    path('<int:pk>/update-status/', update_document_status, name='update_document_status'),
] 