# Generated by Django 3.2 on 2022-07-04 18:44

from django.db import migrations, models
import django.db.models.deletion
import lannister_slack.models


class Migration(migrations.Migration):

    dependencies = [
        ('lannister_slack', '0002_bonusrequest_price_usd'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bonusrequestshistory',
            options={'verbose_name_plural': 'Bonus requests history'},
        ),
        migrations.AlterModelOptions(
            name='bonusrequeststatus',
            options={'verbose_name': 'Bonus status', 'verbose_name_plural': 'Bonus statuses'},
        ),
        migrations.AlterField(
            model_name='bonusrequest',
            name='bonus_type',
            field=models.CharField(choices=[('Referral', 'Referral'), ('Overtime', 'Overtime')], max_length=50),
        ),
        migrations.AlterField(
            model_name='bonusrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='bonusrequest',
            name='price_usd',
            field=models.DecimalField(decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='bonusrequest',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='lannister_slack.bonusrequeststatus'),
        ),
        migrations.AlterField(
            model_name='bonusrequest',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]