# Generated by Django 3.2 on 2022-07-03 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lannister_slack', '0002_auto_20220701_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonusrequest',
            name='payment_date',
            field=models.DateField(null=True),
        ),
    ]
