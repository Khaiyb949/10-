# Generated by Django 5.0.6 on 2024-10-30 02:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dj_app', '0012_alter_taikhoan_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taikhoan',
            name='username',
        ),
    ]
