# Generated by Django 2.2.4 on 2019-11-03 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0010_purchaserequest_specification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='id',
            field=models.CharField(choices=[('NA', 'NOT APPLICABLE'), ('CSE', 'COMPUTER SCIENCE AND ENGINEERING'), ('ECE', 'ELECTRONICS AND COMMUNICATION ENGINEERING'), ('ME', 'MECHANICAL ENGINEERING'), ('EE', 'ELECTRICAL ENGINEERING'), ('EI', 'ELECTRONICS & INSTRUMENTATION ENGINEERING'), ('CE', 'CIVIL ENGINEERING')], default='CSE', max_length=3, primary_key=True, serialize=False),
        ),
    ]