# Generated by Django 3.2 on 2021-10-23 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('id_trust', '0006_journey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dialog',
            name='foil_strategy',
            field=models.CharField(choices=[('C', 'Copy_cat'), ('X', 'Cheat'), ('I', 'Innocent'), ('G', 'Grudger'), ('D', 'Detective')], max_length=1),
        ),
        migrations.AlterField(
            model_name='dialog',
            name='user_guess',
            field=models.CharField(blank=True, choices=[('C', 'Copy_cat'), ('X', 'Cheat'), ('I', 'Innocent'), ('G', 'Grudger'), ('D', 'Detective')], max_length=1),
        ),
    ]