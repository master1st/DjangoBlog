# Generated by Django 3.1.3 on 2022-03-11 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
