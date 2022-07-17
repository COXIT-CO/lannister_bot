# Generated by Django 3.2 on 2022-07-04 17:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BonusRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bonus_type', models.CharField(choices=[('Referral', 'Referral'), ('Overtime', 'Overtime')], max_length=50)),
                ('description', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('price_usd', models.DecimalField(decimal_places=3, max_digits=10)),
                ('payment_date', models.DateTimeField(null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('reviewer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BonusRequestStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(max_length=45, unique=True)),
            ],
            options={
                'verbose_name': 'Bonus status',
                'verbose_name_plural': 'Bonus statuses',
            },
        ),
        migrations.CreateModel(
            name='BonusRequestsHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bonus_request', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='requests', to='lannister_slack.bonusrequest')),
            ],
            options={
                'verbose_name_plural': 'Bonus requests history',
            },
        ),
        migrations.AddField(
            model_name='bonusrequest',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='lannister_slack.bonusrequeststatus'),
        ),
    ]
