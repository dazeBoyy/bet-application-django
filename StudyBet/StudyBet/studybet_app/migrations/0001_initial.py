# Generated by Django 3.0.8 on 2022-10-03 21:18

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Fixture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bet_win', models.CharField(max_length=256)),
                ('bet_lose', models.CharField(max_length=256)),
                ('bet_name', models.CharField(max_length=256)),
                ('fixture_result', models.IntegerField(choices=[(0, 'LOST'), (1, 'WON'), (2, 'PENDING')])),
                ('sum_of_bet', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Bet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bet_amount', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('bet', models.IntegerField(choices=[(0, 'LOST'), (1, 'WON')])),
                ('bet_course', models.IntegerField(default=2)),
                ('bet_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bet_user', to='studybet_app.Account')),
                ('fixture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fixture', to='studybet_app.Fixture')),
            ],
        ),
    ]