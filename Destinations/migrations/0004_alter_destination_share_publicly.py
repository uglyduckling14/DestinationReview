# Generated by Django 4.2.6 on 2023-10-13 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Destinations', '0003_session_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='share_publicly',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
