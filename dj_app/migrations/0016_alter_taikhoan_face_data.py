# Generated by Django 4.2.16 on 2024-11-01 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dj_app', '0015_taikhoan_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taikhoan',
            name='face_data',
            field=models.ImageField(blank=True, null=True, upload_to='truyen_images/'),
        ),
    ]