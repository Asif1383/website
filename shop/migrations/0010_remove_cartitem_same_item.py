# Generated by Django 4.1.5 on 2023-01-09 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_multipleproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='same_item',
        ),
    ]
