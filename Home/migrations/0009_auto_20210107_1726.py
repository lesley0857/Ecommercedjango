# Generated by Django 3.0.2 on 2021-01-07 16:26

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0008_auto_20210107_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='Country',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]
