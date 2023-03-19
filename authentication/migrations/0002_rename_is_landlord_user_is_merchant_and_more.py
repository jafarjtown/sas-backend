# Generated by Django 4.1.7 on 2023-03-14 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_landlord',
            new_name='is_merchant',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='state_of_origin',
            new_name='state_of_resident',
        ),
        migrations.AddField(
            model_name='user',
            name='second_phone_no',
            field=models.CharField(default=0, max_length=11),
            preserve_default=False,
        ),
    ]
