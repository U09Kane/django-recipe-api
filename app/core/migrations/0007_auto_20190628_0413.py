# Generated by Django 2.1.9 on 2019-06-28 04:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_recipe_images'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='images',
            new_name='image',
        ),
    ]
