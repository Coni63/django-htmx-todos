# Generated by Django 5.1.7 on 2025-03-22 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("test_app", "0002_todo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="todo",
            name="completed_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
