# Generated by Django 3.2.1 on 2021-05-11 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raterprojectapi', '0002_game_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='categories',
        ),
        migrations.AlterField(
            model_name='game',
            name='description',
            field=models.CharField(max_length=100),
        ),
    ]