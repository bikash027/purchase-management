# Generated by Django 2.2.4 on 2019-09-09 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0004_auto_20190909_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='statusUpdate',
            field=models.IntegerField(default=0),
        ),
    ]
