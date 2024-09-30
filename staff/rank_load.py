import pandas as pd
from django.db import transaction
from gamification.models import Rank

# Путь к вашему Excel файлу
excel_file_path = "F:\\gamification\\staff\\rank.xlsx"

# Чтение данных из Excel файла без заголовков
df = pd.read_excel(excel_file_path, header=None)

# Переименование столбцов в соответствии с полями в таблице
df.columns = ["title", "level", "required_xp", "bonus_coins"]

# Создание объектов Rank
with transaction.atomic():
    for index, row in df.iterrows():
        Rank.objects.create(
            title=row["title"],
            level=row["level"],
            required_xp=row["required_xp"],
            bonus_coins=row["bonus_coins"],
        )
