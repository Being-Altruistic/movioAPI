# Generated by Django 4.1.3 on 2023-05-13 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist', '0004_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='description',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
