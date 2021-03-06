# Generated by Django 3.1.3 on 2022-06-21 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0011_question_view_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('has_answer', models.BooleanField(default=True)),
            ],
        ),
    ]
