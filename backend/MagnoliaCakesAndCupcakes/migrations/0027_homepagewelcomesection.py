# Generated by Django 4.2.4 on 2023-09-26 08:21

import MagnoliaCakesAndCupcakes.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MagnoliaCakesAndCupcakes', '0026_merge_20230926_0818'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomepageWelcomeSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.TextField()),
                ('paragraph', models.TextField()),
                ('image', models.ImageField(upload_to=MagnoliaCakesAndCupcakes.models.HomepageWelcomeSection.upload_to_welcome)),
            ],
            options={
                'verbose_name_plural': 'Homepage Welcome Section',
            },
        ),
    ]
