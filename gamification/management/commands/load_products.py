import csv
from django.core.management.base import BaseCommand
from gamification.models import Product


class Command(BaseCommand):
    help = "Загружает данные из CSV файла в модель Product"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Путь к CSV файлу")

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]

        try:
            with open(csv_file, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        Product.objects.create(
                            title=row["title"],
                            description=row["description"],
                            price=row["price"],
                            photo=row["photo"],
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
