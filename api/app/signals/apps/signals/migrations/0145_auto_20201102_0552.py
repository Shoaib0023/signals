# Generated by Django 2.2.13 on 2020-11-02 04:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('signals', '0144_auto_20201031_0537'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_level_name1', models.CharField(blank=True, max_length=255, null=True)),
                ('category_level_name2', models.CharField(blank=True, max_length=255, null=True)),
                ('category_level_name3', models.CharField(blank=True, max_length=255, null=True)),
                ('category_level_name4', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='postcode',
            name='neighbourhood',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='postcode', to='signals.Neighbourhood'),
        ),
        migrations.AlterField(
            model_name='postcode',
            name='post_code',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='postcode',
            name='stadsdeelId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='postcode', to='signals.District'),
        ),
        migrations.AddField(
            model_name='signal',
            name='image_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='signal', to='signals.ImageCategory'),
        ),
    ]