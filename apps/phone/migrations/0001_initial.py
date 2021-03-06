# Generated by Django 2.0.3 on 2018-03-22 13:26

import apps.user.utils
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(db_index=True, help_text='Phone number.', max_length=128, unique=True, verbose_name='Phone number')),
                ('is_verified', models.BooleanField(default=False, help_text='Is phone verified.', verbose_name='Verified')),
            ],
            options={
                'verbose_name': 'Phone number',
                'verbose_name_plural': 'Phone numbers',
            },
        ),
        migrations.CreateModel(
            name='PhoneVerificationCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, default=apps.user.utils.generate_pin_code, max_length=4, verbose_name='Code')),
                ('time_expired', models.DateTimeField(db_index=True, default=apps.user.utils.default_time_expired, verbose_name='Time expired')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Creation time')),
                ('phone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phone_verification', to='phone.Phone', verbose_name='Phone')),
            ],
            options={
                'verbose_name': 'Phone verification code',
                'verbose_name_plural': 'Phone verification codes',
            },
        ),
    ]
