# Generated by Django 4.0.5 on 2022-07-06 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_blogpost_related_posts'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='word_list',
            field=models.TextField(default=' '),
            preserve_default=False,
        ),
    ]