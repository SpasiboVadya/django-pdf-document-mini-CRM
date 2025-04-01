from django.db import models
from django.contrib.auth.models import User
from .constants import STATUS_CHOICES, COPY_ORIGINAL_CHOICES, COMPLETENESS_CHOICES


class Document(models.Model):
    """
    Document model representing the main document entity in the system.
    Contains information about documents, their status, and metadata.
    """
    
    # Basic document information
    asset = models.IntegerField(verbose_name="Актив", null=True, blank=True)
    number = models.CharField(max_length=100, verbose_name="Номер документа")
    contractor = models.CharField(max_length=255, verbose_name="Контрагент")
    date = models.DateField(verbose_name="Дата проводки")
    account_number = models.CharField(max_length=50, verbose_name="№ Рахунку", null=True, blank=True)
    doc_type = models.CharField(max_length=50, verbose_name="Тип документа")
    folder = models.CharField(max_length=255, verbose_name="Папка/категорія")
    
    # Status and assignment
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='queue', verbose_name="Статус")
    error_code = models.CharField(max_length=100, blank=True, null=True, verbose_name="Код помилки")
    executer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Виконавець")
    
    # Additional classification
    document_type = models.CharField(max_length=100, verbose_name="Вид документа", blank=True, null=True)
    payment = models.CharField(max_length=100, verbose_name="Платіж", blank=True, null=True)
    document_owner = models.CharField(max_length=100, verbose_name="Власник документа", blank=True, null=True)
    
    # Document attributes
    copy_original = models.CharField(max_length=20, choices=COPY_ORIGINAL_CHOICES, default='copy', verbose_name="Ознака")
    completeness = models.CharField(max_length=20, choices=COMPLETENESS_CHOICES, default='empty', verbose_name="Наповнення")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")
    
    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документи"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['number']),
            models.Index(fields=['folder']),
        ]
    
    def __str__(self):
        return f"{self.number} - {self.contractor}"
    
    def get_status_display_class(self):
        """Return a CSS class based on the status for UI styling."""
        status_classes = {
            'queue': 'bg-secondary',
            'in_progress': 'bg-primary',
            'completed': 'bg-success',
            'error': 'bg-danger',
            'unblocked': 'bg-warning',
            'recognizing': 'bg-info',
        }
        return status_classes.get(self.status, 'bg-secondary')
        

class DocumentPage(models.Model):
    """
    DocumentPage model representing a single page of a document.
    Can contain a file attachment (PDF) and metadata about the page.
    """
    document = models.ForeignKey(Document, related_name='pages', on_delete=models.CASCADE, verbose_name="Документ")
    file_path = models.FileField(upload_to='document_pages/', verbose_name="Файл сторінки")
    page_name = models.CharField(max_length=255, verbose_name="Назва сторінки")
    discrepancy_found = models.BooleanField(default=False, verbose_name="Виявлено розбіжності")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")
    
    class Meta:
        verbose_name = "Сторінка документа"
        verbose_name_plural = "Сторінки документів"
        ordering = ['document', 'id']
        indexes = [
            models.Index(fields=['document']),
        ]
    
    def __str__(self):
        return f"{self.document.number} - {self.page_name}"
    
    @property
    def file_extension(self):
        """Return the file extension of the attached file."""
        return self.file_path.name.split('.')[-1].lower() if self.file_path else None
