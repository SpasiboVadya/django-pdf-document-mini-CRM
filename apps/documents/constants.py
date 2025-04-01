"""
Constants for the documents app.
"""

# Document status choices
STATUS_CHOICES = (
    ('queue', 'На розпізнаванні'),
    ('in_progress', 'Готово до обробки'),
    ('completed', 'Опрацьовані'),
    ('error', 'Помилка'),
    ('unblocked', 'Деблоковано'),
    ('recognizing', 'Розпізнається'),
)

# Document copy/original choices
COPY_ORIGINAL_CHOICES = (
    ('copy', 'Копія'),
    ('original', 'Оригінал'),
)

# Document completeness choices
COMPLETENESS_CHOICES = (
    ('full', 'Пакет повний'),
    ('filling', 'Наповнюється'),
    ('empty', 'Пустий'),
)

# Pagination settings
ITEMS_PER_PAGE = 10 