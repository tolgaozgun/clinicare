# Generated by Django 4.0.5 on 2022-06-17 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_blogpost_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='blogpost_author', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('lastUpdated', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(default='blog/default.png', upload_to='blog')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blogcategory_creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
