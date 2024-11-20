# Generated by Django 4.2.16 on 2024-11-01 09:59

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dj_app', '0016_alter_taikhoan_face_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taikhoan',
            name='face_data',
            field=models.ImageField(blank=True, null=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage(), upload_to='truyen_images/'),
        ),
        migrations.AlterField(
            model_name='taikhoan',
            name='face_encoding',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
