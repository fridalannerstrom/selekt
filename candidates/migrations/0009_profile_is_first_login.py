# Generated by Django 5.2 on 2025-04-28 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0008_remove_candidate_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_first_login',
            field=models.BooleanField(default=True),
        ),
    ]
