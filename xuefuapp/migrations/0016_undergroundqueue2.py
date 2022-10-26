# Generated by Django 3.2.12 on 2022-08-05 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xuefuapp', '0015_port'),
    ]

    operations = [
        migrations.CreateModel(
            name='UndergroundQueue2',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='内部ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='录入日期')),
                ('change_at', models.DateTimeField(auto_now=True, verbose_name='修改日期')),
                ('created_by', models.CharField(blank=True, max_length=20, null=True, verbose_name='录入人员')),
                ('apply_date', models.DateField(blank=True, null=True, verbose_name='申请日期')),
                ('apply_id', models.IntegerField(unique=True, verbose_name='排队申请号')),
                ('process_status', models.IntegerField(choices=[(0, '等待中'), (1, '待办理'), (2, '已办理'), (3, '撤销')], default=1, verbose_name='办理情况')),
                ('complete_date', models.DateField(blank=True, null=True, verbose_name='完成日期')),
                ('notes', models.CharField(blank=True, max_length=100, null=True, verbose_name='备注')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='underground_queue_info_2', to='xuefuapp.car', verbose_name='地库排队2')),
            ],
            options={
                'verbose_name': '地库排队2',
                'verbose_name_plural': '所有地库排队2',
            },
        ),
    ]
