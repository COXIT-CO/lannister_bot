# Generated by Django 3.2 on 2022-07-04 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lannister_slack', '0004_auto_20220704_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonusrequestshistory',
            name='bonus_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='history_requests', to='lannister_slack.bonusrequest'),
        ),
    ]