# Generated by Django 2.2.4 on 2019-11-03 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0011_auto_20191103_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaserequest',
            name='financialYear',
            field=models.IntegerField(default='0'),
        ),
    ]
