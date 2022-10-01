# Generated by Django 3.2.15 on 2022-09-24 15:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_alter_amountingredient_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amountingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amount_ingredients', to='recipes.recipe', verbose_name='recipe'),
        ),
        migrations.AddConstraint(
            model_name='amountingredient',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='unique_amount_ingredient'),
        ),
    ]
