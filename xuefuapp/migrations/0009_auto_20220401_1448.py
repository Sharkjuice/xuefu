# Generated by Django 3.2.12 on 2022-04-01 14:48

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import functools
import xuefuapp.models
import xuefuapp.storage


class Migration(migrations.Migration):

    dependencies = [
        ('xuefuapp', '0008_auto_20220322_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='doc_zulinchengnuoshu',
            field=models.FileField(blank=True, null=True, storage=xuefuapp.storage.OverwriteStorage(), upload_to=functools.partial(xuefuapp.models.gongzhengshu_path, *(2,), **{}), verbose_name='承诺书页面'),
        ),
        migrations.AddField(
            model_name='car',
            name='doc_zulinxiei',
            field=models.FileField(blank=True, null=True, storage=xuefuapp.storage.OverwriteStorage(), upload_to=functools.partial(xuefuapp.models.gongzhengshu_path, *(1,), **{}), verbose_name='租赁协议页面'),
        ),
        migrations.AddField(
            model_name='car',
            name='id',
            field=models.IntegerField(default=0, unique=True, verbose_name='序号'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='car',
            name='new_car',
            field=models.BooleanField(default=False, verbose_name='新车入场'),
        ),
        migrations.AlterField(
            model_name='car',
            name='doc_changzuxieyi_1',
            field=models.FileField(blank=True, null=True, storage=xuefuapp.storage.OverwriteStorage(), upload_to=functools.partial(xuefuapp.models.changzuxieyi_path, *(1,), **{}), verbose_name='长租协议页面1'),
        ),
        migrations.AlterField(
            model_name='car',
            name='doc_changzuxieyi_2',
            field=models.FileField(blank=True, null=True, storage=xuefuapp.storage.OverwriteStorage(), upload_to=functools.partial(xuefuapp.models.changzuxieyi_path, *(2,), **{}), verbose_name='长租协议页面2'),
        ),
        migrations.AlterField(
            model_name='car',
            name='doc_changzuxieyi_3',
            field=models.FileField(blank=True, null=True, storage=xuefuapp.storage.OverwriteStorage(), upload_to=functools.partial(xuefuapp.models.changzuxieyi_path, *(3,), **{}), verbose_name='长租协议页面3'),
        ),
        migrations.AlterField(
            model_name='car',
            name='doc_changzuxieyi_4',
            field=models.FileField(blank=True, null=True, storage=xuefuapp.storage.OverwriteStorage(), upload_to=functools.partial(xuefuapp.models.changzuxieyi_path, *(4,), **{}), verbose_name='长租协议页面4'),
        ),
        migrations.AlterField(
            model_name='car',
            name='doc_changzuxieyi_5',
            field=models.FileField(blank=True, null=True, storage=xuefuapp.storage.OverwriteStorage(), upload_to=functools.partial(xuefuapp.models.changzuxieyi_path, *(5,), **{}), verbose_name='长租协议页面5'),
        ),
        migrations.AlterField(
            model_name='car',
            name='doc_fangchanzheng',
            field=models.FileField(blank=True, null=True, storage=xuefuapp.storage.OverwriteStorage(), upload_to=xuefuapp.models.fangchanzheng_path, verbose_name='房产证'),
        ),
        migrations.AlterField(
            model_name='car',
            name='doc_gongzhengshu_1',
            field=models.FileField(blank=True, null=True, storage=xuefuapp.storage.OverwriteStorage(), upload_to=functools.partial(xuefuapp.models.gongzhengshu_path, *(1,), **{}), verbose_name='公证书页面1'),
        ),
        migrations.AlterField(
            model_name='car',
            name='doc_gongzhengshu_2',
            field=models.FileField(blank=True, null=True, storage=xuefuapp.storage.OverwriteStorage(), upload_to=functools.partial(xuefuapp.models.gongzhengshu_path, *(2,), **{}), verbose_name='公证书页面2'),
        ),
        migrations.AlterField(
            model_name='car',
            name='doc_hukouben_1',
            field=models.FileField(blank=True, null=True, storage=xuefuapp.storage.OverwriteStorage(), upload_to=functools.partial(xuefuapp.models.hukouben_path, *(1,), **{}), verbose_name='户口本页面1'),
        ),
        migrations.AlterField(
            model_name='car',
            name='doc_hukouben_2',
            field=models.FileField(blank=True, null=True, storage=xuefuapp.storage.OverwriteStorage(), upload_to=functools.partial(xuefuapp.models.hukouben_path, *(2,), **{}), verbose_name='户口本页面2'),
        ),
        migrations.AlterField(
            model_name='car',
            name='doc_jiehunzheng',
            field=models.FileField(blank=True, null=True, storage=xuefuapp.storage.OverwriteStorage(), upload_to=xuefuapp.models.jiehunzheng_path, verbose_name='结婚证'),
        ),
        migrations.AlterField(
            model_name='car',
            name='doc_lihunzheng',
            field=models.FileField(blank=True, null=True, storage=xuefuapp.storage.OverwriteStorage(), upload_to=xuefuapp.models.lihunzheng_path, verbose_name='离婚证'),
        ),
        migrations.AlterField(
            model_name='car',
            name='doc_shenfenzheng_1',
            field=models.FileField(blank=True, null=True, storage=xuefuapp.storage.OverwriteStorage(), upload_to=functools.partial(xuefuapp.models.shenfenzheng_path, *(1,), **{}), verbose_name='身份证'),
        ),
        migrations.AlterField(
            model_name='car',
            name='doc_shenfenzheng_2',
            field=models.FileField(blank=True, null=True, storage=xuefuapp.storage.OverwriteStorage(), upload_to=functools.partial(xuefuapp.models.shenfenzheng_path, *(2,), **{}), verbose_name='身份证反面'),
        ),
        migrations.AlterField(
            model_name='car',
            name='doc_xingshizheng',
            field=models.FileField(blank=True, max_length=4000, null=True, storage=xuefuapp.storage.OverwriteStorage(), upload_to=xuefuapp.models.xingshizheng_path, verbose_name='行驶证'),
        ),
    ]
