import csv
from django.core.management.base import BaseCommand
from gamification.models import Rank


class Command(BaseCommand):
    help = "Загружает данные из CSV файла в модель Rank"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Путь к CSV файлу")

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]

        try:
            with open(csv_file, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        Rank.objects.create(
                            title=row["title"],
                            level=row["level"],
                            required_xp=row["required_xp"],
                            bonus_coins=row["bonus_coins"],
                        )
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f"Ошибка при создании объекта: {e}")
                        )

            self.stdout.write(self.style.SUCCESS("Данные успешно загружены"))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("Файл не найден"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Неизвестная ошибка: {e}"))