# Generated by Django 4.1.7 on 2023-03-14 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0002_alter_house_marchant'),
    ]

    operations = [
        migrations.RenameField(
            model_name='house',
            old_name='marchant',
            new_name='merchant',
        ),
    ]