# Generated by Django 2.2.3 on 2019-09-18 01:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20190917_2320'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='meals',
        ),
    ]