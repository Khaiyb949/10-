# Generated by Django 5.0.6 on 2024-08-14 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dj_app', '0003_taikhoan_exp_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='luotxem',
            name='so_luot_xem',
            field=models.IntegerField(default=1),
        ),
    ]