# Generated by Django 3.2 on 2022-07-07 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lannister_slack', '0006_alter_bonusrequestshistory_bonus_request'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bonusrequestshistory',
            name='bonus_request',
        ),
        migrations.RemoveField(
            model_name='bonusrequestshistory',
            name='status',
        ),
        migrations.DeleteModel(
            name='BonusRequest',
        ),
        migrations.DeleteModel(
            name='BonusRequestsHistory',
        ),
        migrations.DeleteModel(
            name='BonusRequestStatus',
        ),
    ]