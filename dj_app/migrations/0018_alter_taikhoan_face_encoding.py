# Generated by Django 4.2.16 on 2024-11-03 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dj_app', '0017_alter_taikhoan_face_data_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taikhoan',
            name='face_encoding',
            field=models.TextField(blank=True, null=True),
        ),
    ]
