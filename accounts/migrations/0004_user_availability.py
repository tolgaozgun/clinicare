# Generated by Django 4.0.5 on 2022-06-21 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_user_isactivated'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='availability',
            field=models.CharField(default='AF0930-1830', max_length=300),
            preserve_default=False,
        ),
    ]
