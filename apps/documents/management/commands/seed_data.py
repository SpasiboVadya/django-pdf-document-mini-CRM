"""
Management command to seed the database with test data.
"""
import random
import os
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.files import File
from django.db import transaction
from django.utils.termcolors import colorize
from tqdm import tqdm

from documents.models import Document, DocumentPage
from documents.constants import STATUS_CHOICES, COPY_ORIGINAL_CHOICES, COMPLETENESS_CHOICES

# Test data constants
CONTRACTORS = [
    "ТОВ НВП ІНН 2345",
    "ПАТ Укрпошта",
    "ТОВ Нова Пошта",
    "ФОП Петренко",
    "ТОВ Розробка",
    "ПП Консалтинг",
    "АТ Банк",
    "ТОВ Логістика",
]

DOC_TYPES = ["Рахунок", "Акт", "Накладна", "Договір", "Специфікація"]
FOLDERS = ["101", "102", "103", "104", "105"]
DOCUMENT_TYPES = ["Рахунок-Фактура", "Видаткова накладна", "Акт виконаних робіт", "Договір про надання послуг"]
PAYMENTS = ["Попередня Оплата", "Післяплата", "Частковий платіж", "Повна оплата"]
OWNERS = ["Коломієць", "Петренко", "Іваненко", "Сидоренко", "Шевченко"]


class Command(BaseCommand):
    """
    Command to seed the database with test documents and users.
    """
    help = 'Seeds the database with sample documents and document pages'

    def add_arguments(self, parser):
        """Define command line arguments."""
        parser.add_argument(
            '--documents', 
            type=int, 
            default=10, 
            help='Number of documents to create'
        )
        parser.add_argument(
            '--pages-per-document', 
            type=int, 
            default=3, 
            help='Number of pages per document'
        )
        parser.add_argument(
            '--image-path', 
            type=str, 
            default='sample.png', 
            help='Path to the image file to use for pages'
        )
        parser.add_argument(
            '--no-progress', 
            action='store_true',
            help='Disable progress bar'
        )

    def _create_test_user(self):
        """Create a test user if it doesn't exist."""
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Created test user: testuser (password: testpass123)')
            )
        
        return user

    def _verify_image_path(self, image_path):
        """Verify that the image file exists at the specified path."""
        if not os.path.exists(image_path):
            raise CommandError(f'Image file not found at path: {image_path}')
        
        return image_path

    def _create_document(self, index, user):
        """Create a single document with random data."""
        return Document.objects.create(
            number=f'2000{str(index+1).zfill(5)}',
            contractor=random.choice(CONTRACTORS),
            date=datetime.now() - timedelta(days=random.randint(0, 365)),
            doc_type=random.choice(DOC_TYPES),
            folder=random.choice(FOLDERS),
            status=random.choice([s[0] for s in STATUS_CHOICES]),
            executer=user if random.choice([True, False]) else None,
            document_type=random.choice(DOCUMENT_TYPES),
            payment=random.choice(PAYMENTS),
            document_owner=random.choice(OWNERS),
            asset=random.randint(1000, 9999),
            account_number=f'UA{str(random.randint(10000, 99999))}',
            copy_original=random.choice([c[0] for c in COPY_ORIGINAL_CHOICES]),
            completeness=random.choice([c[0] for c in COMPLETENESS_CHOICES])
        )

    def _create_document_page(self, document, page_index, image_path):
        """Create a single document page with image attachment."""
        page = DocumentPage(
            document=document,
            page_name=f'Сторінка {page_index+1}',
            discrepancy_found=random.choice([True, False])
        )
        
        # Attach the image file to the DocumentPage
        try:
            with open(image_path, 'rb') as image_file:
                page.file_path.save(
                    f'document_{document.id}_page_{page_index+1}.png',
                    File(image_file),
                    save=True
                )
            self.stdout.write(f'Attached image to document {document.id}, page {page_index+1}')
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error attaching image file: {str(e)}'))
            page.save()  # Save the page without the file
        
        return page

    def handle(self, *args, **options):
        """Main command handler."""
        # Get command arguments
        num_documents = options['documents']
        pages_per_document = options['pages_per_document']
        image_path = options['image_path']
        show_progress = not options['no_progress']
        
        # Setup
        user = self._create_test_user()
        image_path = self._verify_image_path(image_path)
        
        # Create documents within a transaction
        try:
            with transaction.atomic():
                if show_progress:
                    doc_iter = tqdm(range(num_documents), desc="Creating documents")
                else:
                    doc_iter = range(num_documents)
                
                for i in doc_iter:
                    # Create document
                    doc = self._create_document(i, user)
                    
                    # Create pages for each document
                    for j in range(pages_per_document):
                        self._create_document_page(doc, j, image_path)
                    
                    if not show_progress:
                        self.stdout.write(f'Created document {i+1}/{num_documents} with {pages_per_document} pages')
            
            self.stdout.write(self.style.SUCCESS(
                f'Successfully created {num_documents} documents with {pages_per_document} pages each'
            ))
            
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error creating data: {str(e)}'))
            raise CommandError(f'Failed to seed database: {str(e)}') 