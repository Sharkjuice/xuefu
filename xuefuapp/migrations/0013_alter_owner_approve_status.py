# Generated by Django 3.2.12 on 2022-04-03 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xuefuapp', '0012_auto_20220403_0144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='approve_status',
            field=models.IntegerField(choices=[(1, '待核验'), (2, '通过'), (3, '不通过'), (5, '资料不全'), (4, '欠费')], default=1, verbose_name='确认状态'),
        ),
    ]
