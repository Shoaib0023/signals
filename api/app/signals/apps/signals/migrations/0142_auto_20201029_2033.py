# Generated by Django 2.2.13 on 2020-10-29 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signals', '0141_auto_20201020_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='descriptionId',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='district',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
