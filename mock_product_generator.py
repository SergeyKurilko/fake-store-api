import random

# Категории продуктов
CATEGORIES = [
    "electronics",
    "jewelery",
    "men's clothing",
    "women's clothing",
    "sports",
    "books",
    "toys",
    "home",
]

# Префиксы для названий
TITLE_PREFIXES = {
    "electronics": [
        "Смартфон",
        "Ноутбук",
        "Планшет",
        "Наушники",
        "Колонка",
        "Монитор",
        "Клавиатура",
        "Мышь",
        "Зарядное устройство",
        "Внешний диск",
    ],
    "jewelery": [
        "Кольцо",
        "Серьги",
        "Цепочка",
        "Браслет",
        "Подвеска",
        "Кулон",
        "Запонки",
        "Брошь",
    ],
    "men's clothing": [
        "Куртка",
        "Джинсы",
        "Футболка",
        "Рубашка",
        "Свитер",
        "Пиджак",
        "Брюки",
        "Шорты",
        "Кепка",
        "Ремень",
    ],
    "women's clothing": [
        "Платье",
        "Юбка",
        "Блузка",
        "Топ",
        "Пальто",
        "Леггинсы",
        "Джемпер",
        "Сарафан",
        "Шарф",
        "Сумка",
    ],
    "sports": [
        "Беговые кроссовки",
        "Футбольный мяч",
        "Тренажер",
        "Гантели",
        "Коврик для йоги",
        "Велосипед",
        "Лыжи",
        "Ракетка",
        "Плавательные очки",
        "Спортивный костюм",
    ],
    "books": [
        "Роман",
        "Детектив",
        "Фантастика",
        "Учебник",
        "Энциклопедия",
        "Кулинарная книга",
        "Биография",
        "Поэзия",
        "Комикс",
        "Журнал",
    ],
    "toys": [
        "Конструктор",
        "Кукла",
        "Машинка",
        "Мягкая игрушка",
        "Пазл",
        "Настольная игра",
        "Робот",
        "Поезд",
        "Мозаика",
        "Дрон",
    ],
    "home": [
        "Диван",
        "Стул",
        "Стол",
        "Шкаф",
        "Комод",
        "Кровать",
        "Тумба",
        "Стеллаж",
        "Лампа",
        "Ковер",
    ],
}


def generate_mock_products(count: int = 100) -> list:
    """Генерирует список моковых продуктов"""
    products = []

    for i in range(1, count + 1):
        # Выбираем случайную категорию
        category = random.choice(CATEGORIES)

        # Выбираем префикс для названия из соответствующей категории
        prefix = random.choice(TITLE_PREFIXES[category])

        # Генерируем название с номером
        title = f"{prefix} {random.choice(['Premium', 'Pro', 'Lux', 'Classic', 'Sport', 'Comfort', 'Style'])} {i}"

        # Генерируем цену (от 10 до 2000)
        price = random.randint(10, 2000)

        # Генерируем описание в зависимости от категории
        descriptions = {
            "electronics": "Современное устройство с передовыми технологиями. Высокое качество и надежность.",
            "jewelery": "Изящное украшение из высококачественных материалов. Отличный подарок.",
            "men's clothing": "Качественная одежда для настоящих мужчин. Стиль и комфорт.",
            "women's clothing": "Элегантная женская одежда из натуральных тканей. Подчеркнет ваш стиль.",
            "sports": "Профессиональное спортивное снаряжение. Поможет достичь новых высот.",
            "books": "Увлекательная книга, которая не оставит вас равнодушным.",
            "toys": "Безопасная и интересная игрушка для детей любого возраста.",
            "home": "Качественная мебель для вашего дома. Создайте уютную атмосферу.",
        }

        description = (
            descriptions[category] + f" Артикул: {random.randint(10000, 99999)}"
        )

        # Генерируем URL изображения
        image = f"https://myfakestoreapi.com/img/{random.randint(1, 500)}.jpg"

        # Генерируем рейтинг
        rate = round(random.uniform(1.0, 5.0), 1)
        rating_count = random.randint(10, 2000)

        product = {
            "title": title,
            "price": price,
            "description": description,
            "category": category,
            "image": image,
            "rating": {"rate": rate, "count": rating_count},
        }

        products.append(product)

    return products


# Использование:
mock_products = generate_mock_products(5000)

# Пример для проверки первых 3 продуктов:
# print(mock_products[:3])
a = 15
for mock_product in mock_products:
    print(f"\t{mock_product},")

# # Функция для создания продуктов в БД
# def create_fake_products(session):
#     """Создает продукты в базе данных"""
#     from database.models import FakeProduct
#
#     mock_products = generate_mock_products(100)
#
#     for mock_product in mock_products:
#         new_product = FakeProduct(**mock_product)
#         session.add(new_product)
#
#     session.commit()
#     return len(mock_products)
