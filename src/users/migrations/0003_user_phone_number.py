# Generated by Django 5.0.9 on 2024-09-10 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_user_options_alter_user_table"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="phone_number",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
