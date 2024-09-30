# Generated by Django 5.1.1 on 2024-09-30 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamification', '0002_achievement_coins_reward_alter_userprofile_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='xp',
            field=models.PositiveIntegerField(default=0, help_text='Опыт команды', verbose_name='Опыт'),
        ),
        migrations.AlterField(
            model_name='achievement',
            name='coins_reward',
            field=models.PositiveIntegerField(help_text='Количество монет за получение достижения', null=True, verbose_name='Награда за выполнение (монеты)'),
        ),
        migrations.AlterField(
            model_name='achievement',
            name='xp_reward',
            field=models.PositiveIntegerField(help_text='Количество опыта за получение достижения', verbose_name='Награда за выполнение (XP)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.PositiveIntegerField(default=0, help_text='Цена товара', verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='task',
            name='xp_reward',
            field=models.PositiveIntegerField(help_text='Количество опыта за выполнение задачи', verbose_name='Награда за выполнение (XP)'),
        ),
    ]
