# Generated by Django 4.0.5 on 2022-06-10 10:58

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0006_report_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(default='product/default.png', upload_to='product')),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='is2FAEnabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='isActivated',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='lastLogin',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='panel.product')),
                ('quantity', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
            ],
            bases=('panel.product',),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderNo', models.CharField(max_length=40)),
                ('customer', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='order_customer', to=settings.AUTH_USER_MODEL)),
                ('products', models.ManyToManyField(to='panel.product')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointmentDate', models.DateTimeField(null=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('lastUpdated', models.DateTimeField(auto_now=True)),
                ('doctor', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_doctor', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_patient', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]