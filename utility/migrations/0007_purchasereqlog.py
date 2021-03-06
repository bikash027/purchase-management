# Generated by Django 2.2.4 on 2019-09-11 02:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0006_auto_20190909_1944'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseReqLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('changedTo', models.IntegerField(choices=[(0, 'Purchase Request Saved in Draft'), (1, 'Purchase Request is with HOD'), (2, 'Waiting for approval by HOD'), (3, 'Purchase Request is in Account Section'), (4, 'Waiting for Approval by Account Section'), (5, 'Waiting for Approval by Registrar'), (6, 'Waiting for Approval by Director'), (7, 'Approved by Account Section'), (8, 'Purchase Request at Purchase Section'), (9, 'Product Purchased'), (10, 'Purchase denied')], default=1)),
                ('comments', models.TextField(blank=True, null=True)),
                ('purchaseRequest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utility.PurchaseRequest')),
            ],
        ),
    ]
