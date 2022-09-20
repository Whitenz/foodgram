"""Менеджмент-команда для наполнения БД данными из csv-файла."""

import csv

from django.core.management import BaseCommand

from recipes.models import Ingredient

ALREADY_LOADED_ERROR_MESSAGE = 'Таблица уже имеет записи, наполнить нельзя.'


class Command(BaseCommand):
    help = 'Заполняет таблицу Ingredient в БД из csv файла'

    def handle(self, *args, **options):
        if Ingredient.objects.exists():
            self.stdout.write(ALREADY_LOADED_ERROR_MESSAGE)
            return

        self.stdout.write('Загрузка данных в таблицу Ingredient')
        with open('./ingredients.csv', encoding='utf-8') as csvfile:
            ingredient_reader = csv.reader(csvfile, delimiter=',')
            for row in ingredient_reader:
                ingredient = Ingredient(name=row[0], measurement_unit=row[1])
                ingredient.save()

            self.stdout.write(
                f'Записей после вставки: {Ingredient.objects.all().count()}'
            )

