# Generated by Django 5.0.1 on 2024-02-07 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Bookapi', '0006_customuser'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'permissions': [('book_add_book', 'Can add book'), ('book_change_book', 'Can change book'), ('book_delete_book', 'Can delete book')]},
        ),
    ]
