# Generated by Django 3.2.12 on 2022-04-01 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xuefuapp', '0010_auto_20220401_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='car_of',
            field=models.IntegerField(choices=[('业主', 1), ('租户', 2)], default=1, verbose_name='业主/租户'),
        ),
    ]
