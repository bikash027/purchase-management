# Generated by Django 2.2.4 on 2019-09-09 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0005_auto_20190909_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]