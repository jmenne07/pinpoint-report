# Generated by Django 5.1.4 on 2025-01-15 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('georeport', '0006_alter_category_options_group'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Group',
        ),
    ]
