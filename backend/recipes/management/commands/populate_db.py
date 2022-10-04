"""Management command for filling the database with data from a csv-file."""

import csv
import os

from django.conf import settings
from django.core.management import BaseCommand, CommandError
from django.utils.translation import gettext_lazy as _

from recipes.models import Ingredient


class Command(BaseCommand):
    help = _('Fills Ingredient table from a csv file')
    messages = {
        'already_loaded_error': _('The data in the table already exists'),
        'loading_data': _('Loading data into the table "Ingredient"'),
        'file_does_not_exist': _('The data file for database does not exist'),
        'fields_error': _('Number of fields in the file does not match'),
        'success_loading': _('Successful data upload'),
        'count_data': _('Entities in the table after loading - {}'.format(
            Ingredient.objects.all().count())
        ),
    }
    # set path to csv-file for populate with ingredients
    path = settings.BASE_DIR / 'recipes/management/commands/ingredients.csv'
    # set how many fields in the table Ingredient
    count_fields = 2

    def handle(self, *args, **options):
        if not os.path.isfile(self.path):
            raise CommandError(self.messages.get('file_does_not_exist'))
        if Ingredient.objects.exists():
            raise CommandError(self.messages.get('already_loaded_error'))

        self.stdout.write(self.messages.get('loading_data'))
        ingredients_list = []
        with open(self.path, encoding='utf-8') as csvfile:
            ingredient_reader = csv.reader(csvfile, delimiter=',')
            for row in ingredient_reader:
                if len(row) != self.count_fields:
                    raise CommandError(self.messages.get('fields_error'))
                ingredients_list.append(
                    Ingredient(name=row[0], measurement_unit=row[1])
                )
        Ingredient.objects.bulk_create(ingredients_list)

        self.stdout.write(self.style.SUCCESS(
            self.messages.get('success_loading'))
        )
        self.stdout.write(self.style.SUCCESS(
            self.messages.get('count_data'))
        )
