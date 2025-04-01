# Generated by Django 4.2.20 on 2025-04-01 15:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset', models.IntegerField(blank=True, null=True, verbose_name='Актив')),
                ('number', models.CharField(max_length=100, verbose_name='Номер документа')),
                ('contractor', models.CharField(max_length=255, verbose_name='Контрагент')),
                ('date', models.DateField(verbose_name='Дата проводки')),
                ('account_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='№ Рахунку')),
                ('doc_type', models.CharField(max_length=50, verbose_name='Тип документа')),
                ('folder', models.CharField(max_length=255, verbose_name='Папка/категорія')),
                ('status', models.CharField(choices=[('queue', 'На розпізнаванні'), ('in_progress', 'Готово до обробки'), ('completed', 'Опрацьовані'), ('error', 'Помилка'), ('unblocked', 'Деблоковано'), ('recognizing', 'Розпізнається')], default='queue', max_length=20, verbose_name='Статус')),
                ('error_code', models.CharField(blank=True, max_length=100, null=True, verbose_name='Код помилки')),
                ('document_type', models.CharField(blank=True, max_length=100, null=True, verbose_name='Вид документа')),
                ('payment', models.CharField(blank=True, max_length=100, null=True, verbose_name='Платіж')),
                ('document_owner', models.CharField(blank=True, max_length=100, null=True, verbose_name='Власник документа')),
                ('copy_original', models.CharField(choices=[('copy', 'Копія'), ('original', 'Оригінал')], default='copy', max_length=20, verbose_name='Ознака')),
                ('completeness', models.CharField(choices=[('full', 'Пакет повний'), ('filling', 'Наповнюється'), ('empty', 'Пустий')], default='empty', max_length=20, verbose_name='Наповнення')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Створено')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Оновлено')),
                ('executer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Виконавець')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документи',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='DocumentPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.FileField(upload_to='document_pages/', verbose_name='Файл сторінки')),
                ('page_name', models.CharField(max_length=255, verbose_name='Назва сторінки')),
                ('discrepancy_found', models.BooleanField(default=False, verbose_name='Виявлено розбіжності')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Створено')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Оновлено')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='documents.document', verbose_name='Документ')),
            ],
            options={
                'verbose_name': 'Сторінка документа',
                'verbose_name_plural': 'Сторінки документів',
                'ordering': ['document', 'id'],
            },
        ),
    ]
