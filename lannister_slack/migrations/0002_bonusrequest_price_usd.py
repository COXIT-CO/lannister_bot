# Generated by Django 3.2 on 2022-07-01 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lannister_slack', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bonusrequest',
            name='price_usd',
            field=models.DecimalField(decimal_places=3, default=100.0, max_digits=10),
            preserve_default=False,
        ),
    ]
