# Generated by Django 4.1.3 on 2022-12-02 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cat_linebot', '0011_alter_user_info_ansdt'),
    ]

    operations = [
        migrations.AddField(
            model_name='toy',
            name='pic_url',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
