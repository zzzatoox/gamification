# Generated by Django 5.1.1 on 2024-09-29 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamification', '0003_user_patronymic'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]