# Generated by Django 3.1.3 on 2022-06-21 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0013_question_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['id']},
        ),
        migrations.AlterField(
            model_name='question',
            name='view_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]