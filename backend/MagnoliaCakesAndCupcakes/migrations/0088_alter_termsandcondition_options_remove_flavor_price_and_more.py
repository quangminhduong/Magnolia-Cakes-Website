# Generated by Django 4.2.4 on 2023-10-19 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MagnoliaCakesAndCupcakes', '0087_rename_product_flavor_product_item_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='termsandcondition',
            options={'ordering': ['id'], 'verbose_name_plural': 'Terms And Conditions'},
        ),
        migrations.RemoveField(
            model_name='flavor',
            name='price',
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
