# Generated by Django 2.2.3 on 2019-09-14 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address2',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]