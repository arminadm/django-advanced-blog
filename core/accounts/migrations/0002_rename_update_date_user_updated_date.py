# Generated by Django 3.2.13 on 2022-06-11 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='update_date',
            new_name='updated_date',
        ),
    ]