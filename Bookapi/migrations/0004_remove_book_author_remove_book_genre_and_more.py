# Generated by Django 5.0.1 on 2024-01-29 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Bookapi', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.RemoveField(
            model_name='book',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='book',
            name='library',
        ),
        migrations.DeleteModel(
            name='Genre',
        ),
        migrations.DeleteModel(
            name='Book',
        ),
    ]
