# Generated by Django 5.1.3 on 2024-11-13 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="answer",
            name="rating",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="question",
            name="rating",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="profile",
            name="avatar",
            field=models.ImageField(blank=True, upload_to="./uploads/"),
        ),
        migrations.AlterField(
            model_name="question",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="questions", to="app.tag"
            ),
        ),
    ]
