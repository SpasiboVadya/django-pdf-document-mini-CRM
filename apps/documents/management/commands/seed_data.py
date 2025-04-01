import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from documents.models import Document, DocumentPage
from django.core.files import File
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def add_arguments(self, parser):
        parser.add_argument('--documents', type=int, default=10, help='Number of documents to create')
        parser.add_argument('--pages-per-document', type=int, default=3, help='Number of pages per document')

    def handle(self, *args, **options):
        # Create a test user if it doesn't exist
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
            self.stdout.write(self.style.SUCCESS(f'Created test user: testuser (password: testpass123)'))

        # Sample data
        contractors = [
            "ТОВ НВП ІНН 2345",
            "ПАТ Укрпошта",
            "ТОВ Нова Пошта",
            "ФОП Петренко",
            "ТОВ Розробка",
            "ПП Консалтинг",
            "АТ Банк",
            "ТОВ Логістика",
        ]

        doc_types = ["Рахунок", "Акт", "Накладна", "Договір", "Специфікація"]
        folders = ["101", "102", "103", "104", "105"]
        document_types = ["Рахунок-Фактура", "Видаткова накладна", "Акт виконаних робіт", "Договір про надання послуг"]
        payments = ["Попередня Оплата", "Післяплата", "Частковий платіж", "Повна оплата"]
        owners = ["Коломієць", "Петренко", "Іваненко", "Сидоренко", "Шевченко"]

        # Create documents
        num_documents = options['documents']
        pages_per_document = options['pages_per_document']

        for i in range(num_documents):
            # Create document
            doc = Document.objects.create(
                number=f'2000{str(i+1).zfill(5)}',
                contractor=random.choice(contractors),
                date=datetime.now() - timedelta(days=random.randint(0, 365)),
                doc_type=random.choice(doc_types),
                folder=random.choice(folders),
                status=random.choice([s[0] for s in Document.STATUS_CHOICES]),
                executer=user if random.choice([True, False]) else None,
                document_type=random.choice(document_types),
                payment=random.choice(payments),
                document_owner=random.choice(owners),
                asset=random.randint(1000, 9999),
                account_number=f'UA{str(random.randint(10000, 99999))}',
                copy_original=random.choice(['copy', 'original']),
                completeness=random.choice(['full', 'filling', 'empty'])
            )

            # Create pages for the document
            for j in range(pages_per_document):
                page = DocumentPage.objects.create(
                    document=doc,
                    page_name=f'Сторінка {j+1}',
                    discrepancy_found=random.choice([True, False])
                )

            self.stdout.write(f'Created document {i+1}/{num_documents} with {pages_per_document} pages')

        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_documents} documents with {pages_per_document} pages each')) 