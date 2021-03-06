# Generated by Django 4.0.5 on 2022-06-17 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
                ('text', models.TextField()),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('lastUpdated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
