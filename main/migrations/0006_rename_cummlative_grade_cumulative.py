# Generated by Django 4.2.1 on 2023-06-05 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_grade_cummlative_grade_semigrade'),
    ]

    operations = [
        migrations.RenameField(
            model_name='grade',
            old_name='cummlative',
            new_name='cumulative',
        ),
    ]
