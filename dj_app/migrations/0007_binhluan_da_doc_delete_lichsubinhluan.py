# Generated by Django 5.0.6 on 2024-08-16 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dj_app', '0006_lichsubinhluan'),
    ]

    operations = [
        migrations.AddField(
            model_name='binhluan',
            name='da_doc',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='LichSuBinhLuan',
        ),
    ]
