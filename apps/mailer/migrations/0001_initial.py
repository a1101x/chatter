# Generated by Django 2.0.3 on 2018-03-12 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.IntegerField(choices=[(100, 'User activation'), (200, 'Forgot password'), (300, 'Change email')], db_index=True, help_text='Email type.', unique=True, verbose_name='Key')),
                ('subject', models.CharField(db_index=True, help_text='Email subject.', max_length=255, verbose_name='Subject')),
                ('title', models.CharField(db_index=True, help_text='Email title.', max_length=255, verbose_name='Title')),
                ('body', models.TextField(db_index=True, help_text='Email body.', verbose_name='Content')),
                ('button_label', models.CharField(blank=True, db_index=True, help_text='Template button label.', max_length=255, verbose_name='Button label')),
                ('button_link', models.CharField(blank=True, db_index=True, help_text='Template button link.', max_length=255, verbose_name='Button Link')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, help_text='Template creation date.', verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, help_text='Template update date.', verbose_name='Updated at')),
                ('is_active', models.BooleanField(default=True, help_text='Is template active.', verbose_name='Active')),
            ],
            options={
                'verbose_name': 'E-mail template',
                'verbose_name_plural': 'E-mail templates',
            },
        ),
    ]
