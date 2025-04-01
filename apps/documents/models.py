from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    STATUS_CHOICES = (
        ('queue', 'На розпізнаванні'),
        ('in_progress', 'Готово до обробки'),
        ('completed', 'Опрацьовані'),
        ('error', 'Помилка'),
        ('unblocked', 'Деблоковано'),
        ('recognizing', 'Розпізнається'),
    )
    
    asset = models.IntegerField(verbose_name="Актив", null=True, blank=True)
    number = models.CharField(max_length=100, verbose_name="Номер документа")
    contractor = models.CharField(max_length=255, verbose_name="Контрагент")
    date = models.DateField(verbose_name="Дата проводки")
    account_number = models.CharField(max_length=50, verbose_name="№ Рахунку", null=True, blank=True)
    doc_type = models.CharField(max_length=50, verbose_name="Тип документа")
    folder = models.CharField(max_length=255, verbose_name="Папка/категорія")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='queue', verbose_name="Статус")
    error_code = models.CharField(max_length=100, blank=True, null=True, verbose_name="Код помилки")
    executer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Виконавець")
    
    # Службові поля
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")
    
    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документи"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.number} - {self.contractor}"


class DocumentPage(models.Model):
    COPY_ORIGINAL_CHOICES = (
        ('copy', 'Копія'),
        ('original', 'Оригінал'),
    )
    
    COMPLETENESS_CHOICES = (
        ('full', 'Пакет повний'),
        ('filling', 'Наповнюється'),
        ('empty', 'Пустий'),
    )
    
    document = models.ForeignKey(Document, related_name='pages', on_delete=models.CASCADE, verbose_name="Документ")
    file_path = models.FileField(upload_to='document_pages/', verbose_name="Файл сторінки")
    page_name = models.CharField(max_length=255, verbose_name="Назва сторінки")
    discrepancy_found = models.BooleanField(default=False, verbose_name="Виявлено розбіжності")
    
    # Додаткові поля
    copy_original = models.CharField(max_length=20, choices=COPY_ORIGINAL_CHOICES, default='copy', verbose_name="Ознака")
    completeness = models.CharField(max_length=20, choices=COMPLETENESS_CHOICES, default='empty', verbose_name="Наповнення")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")
    
    class Meta:
        verbose_name = "Сторінка документа"
        verbose_name_plural = "Сторінки документів"
        ordering = ['document', 'id']
    
    def __str__(self):
        return f"{self.document.number} - {self.page_name}"
