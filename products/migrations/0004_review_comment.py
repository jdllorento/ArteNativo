# Generated by Django 4.2.7 on 2025-03-20 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0003_review"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="comment",
            field=models.TextField(blank=True, null=True),
        ),
    ]
