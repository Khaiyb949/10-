# Generated by Django 5.0.6 on 2024-08-15 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dj_app', '0004_luotxem_so_luot_xem'),
    ]

    operations = [
        migrations.AddField(
            model_name='taikhoan',
            name='level_system',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
