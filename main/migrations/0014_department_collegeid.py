# Generated by Django 4.2.2 on 2023-06-08 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_withdraw_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='collegeid',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
