# Generated by Django 3.2.12 on 2022-03-21 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xuefuapp', '0003_alter_undergroundqueue_process_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='approve_status',
            field=models.IntegerField(choices=[(1, '待核实'), (2, '通过'), (3, '不通过'), (4, '无数据')], default=1, verbose_name='审核状态'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='approve_status',
            field=models.IntegerField(blank=True, choices=[(1, '待核实'), (2, '通过'), (3, '不通过'), (4, '无数据')], null=True, verbose_name='确认状态'),
        ),
    ]
