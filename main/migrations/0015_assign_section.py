# Generated by Django 4.2.2 on 2023-06-12 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_department_collegeid'),
    ]

    operations = [
        migrations.AddField(
            model_name='assign',
            name='section',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
