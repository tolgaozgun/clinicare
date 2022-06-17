# Generated by Django 4.0.5 on 2022-06-16 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescription',
            name='files',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.AlterField(
            model_name='appointment',
            name='appointmentDate',
            field=models.DateTimeField(),
        ),
        migrations.RemoveField(
            model_name='report',
            name='files',
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(default='profile/avatar.png', null=True, upload_to='profile'),
        ),
        migrations.CreateModel(
            name='ReportFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='attachments/reports')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_file_report', to='panel.report')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(default='product/default.png', upload_to='product')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_image_product', to='panel.product')),
            ],
        ),
        migrations.CreateModel(
            name='PrescriptionFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='attachments/prescriptions')),
                ('prescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescription_file_prescription', to='panel.prescription')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='coverImage',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='product_cover_image', to='panel.productimage'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ManyToManyField(related_name='product_images', to='panel.productimage'),
        ),
        migrations.AddField(
            model_name='report',
            name='files',
            field=models.ManyToManyField(related_name='report_files', to='panel.reportfile'),
        ),
    ]