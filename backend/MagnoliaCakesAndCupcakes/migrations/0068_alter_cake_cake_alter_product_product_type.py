# Generated by Django 4.2.4 on 2023-10-16 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MagnoliaCakesAndCupcakes', '0067_rename_cakesizeprice_cake'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cake',
            name='cake',
            field=models.ForeignKey(limit_choices_to={'product_type': 'Cake'}, on_delete=django.db.models.deletion.CASCADE, related_name='size_prices', to='MagnoliaCakesAndCupcakes.product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(choices=[('Cake', 'Cake'), ('Cupcake', 'Cupcake')], default='Cake', max_length=10),
        ),
    ]
