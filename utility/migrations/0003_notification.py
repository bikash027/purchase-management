# Generated by Django 2.2.4 on 2019-09-09 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0002_auto_20190905_0034'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen', models.CharField(choices=[('N', 'NO'), ('Y', 'YES')], default='N', max_length=1)),
                ('statusUpdate', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('purchaseRequest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utility.PurchaseRequest')),
            ],
        ),
    ]
