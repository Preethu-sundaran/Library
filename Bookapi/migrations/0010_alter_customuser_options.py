# Generated by Django 5.0.1 on 2024-02-07 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Bookapi', '0009_alter_book_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'permissions': [('create_book', 'Can create book'), ('modify_book', 'Can modify book'), ('destroy_book', 'Can destroy book')]},
        ),
    ]
