# Generated by Django 4.0.5 on 2022-07-06 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogpost_author_blogcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='related_posts',
            field=models.ManyToManyField(to='blog.blogpost'),
        ),
    ]
