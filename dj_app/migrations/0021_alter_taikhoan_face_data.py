# Generated by Django 4.2.16 on 2024-11-19 06:15

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dj_app', '0020_alter_taikhoan_face_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taikhoan',
            name='face_data',
            field=models.ImageField(blank=True, null=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage(), upload_to='truyen_images/'),
        ),
    ]
