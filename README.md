# PDF Document Mini CRM

Простий Django застосунок для управління PDF документами (міні-CRM система).

## Опис проекту

Цей проект реалізує систему управління документами з наступними можливостями:
- Відображення списку документів з фільтрами та сортуванням
- Детальний перегляд документів з інформацією та прикріпленими файлами
- Управління статусами документів
- Адміністративна панель для повного керування

## Структура проекту

Проект має наступну структуру директорій:
```
django-pdf-document-mini-CRM/
├── apps/                     # Директорія для всіх застосунків Django
│   ├── __init__.py
│   └── documents/            # Застосунок для роботи з документами
├── config/                   # Налаштування проекту
├── media/                    # Директорія для завантажених файлів
├── templates/                # Глобальні шаблони
│   ├── base.html             # Базовий шаблон
│   └── documents/            # Шаблони для документів
├── manage.py
└── README.md
```

## Моделі

### Document
- number - номер документа
- contractor - контрагент
- date - дата документа
- doc_type - тип документа
- folder - папка/категорія
- status - статус документа
- error_code - код помилки
- executer - виконавець

### DocumentPage
- document - зв'язок з документом
- file_path - файл сторінки
- page_name - назва сторінки
- discrepancy_found - ознака розбіжностей
- copy_original - ознака (копія/оригінал)
- completeness - наповнення (повний/наповнюється/пустий)

## Встановлення та запуск

1. Клонуйте репозиторій:
```
git clone https://github.com/username/django-pdf-document-mini-CRM.git
cd django-pdf-document-mini-CRM
```

2. Встановіть залежності:
```
pip install -r requirements.txt
```

3. Виконайте міграції:
```
python manage.py migrate
```

4. Створіть суперкористувача:
```
python manage.py createsuperuser
```

5. Запустіть сервер розробки:
```
python manage.py runserver
```

6. Відкрийте браузер за адресою http://127.0.0.1:8000/

## Технології
- Python 3.8+
- Django 4.2+
- Bootstrap 5
- HTML/CSS/JavaScript 