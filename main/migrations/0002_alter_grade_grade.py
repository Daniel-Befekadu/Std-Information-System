# Generated by Django 4.2.1 on 2023-06-05 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='grade',
            field=models.CharField(max_length=4, null=True),
        ),
    ]
