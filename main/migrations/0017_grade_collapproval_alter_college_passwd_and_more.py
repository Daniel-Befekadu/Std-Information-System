# Generated by Django 4.2.2 on 2023-06-18 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_remove_student_grade10_remove_student_grade11_12_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='collapproval',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='college',
            name='passwd',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='department',
            name='passwd',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='passwd',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='registrar',
            name='passwd',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='passwd',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
