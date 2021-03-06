# Generated by Django 3.1 on 2020-10-25 13:19

from django.db import migrations, models


def noop(apps, schema_editor):
    pass


def effect_is_intent(apps, schema_editor):
    Exchange = apps.get_model('id_trust', 'Exchange')
    Exchange.objects.update(user_effect=models.F('user_intent'))
    Exchange.objects.update(foil_effect=models.F('foil_intent'))
    

class Migration(migrations.Migration):

    dependencies = [
        ('id_trust', '0003_interaction_user_guess'),
    ]

    operations = [
        migrations.AddField(
            model_name='exchange',
            name='foil_effect',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.RenameField(
            model_name='exchange',
            old_name='foil_trust',
            new_name='foil_intent',
        ),
        migrations.AddField(
            model_name='exchange',
            name='user_effect',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.RenameField(
            model_name='exchange',
            old_name='user_trust',
            new_name='user_intent',
        ),
        migrations.AddField(
            model_name='interaction',
            name='foil_miscommunication',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='interaction',
            name='user_miscommunication',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.RunPython(effect_is_intent, noop)
    ]
