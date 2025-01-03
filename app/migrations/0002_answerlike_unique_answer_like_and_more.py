# Generated by Django 5.1.3 on 2024-12-24 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='answerlike',
            constraint=models.UniqueConstraint(fields=('answer', 'user'), name='unique_answer_like'),
        ),
        migrations.AddConstraint(
            model_name='questionlike',
            constraint=models.UniqueConstraint(fields=('question', 'user'), name='unique_question_like'),
        ),
    ]
