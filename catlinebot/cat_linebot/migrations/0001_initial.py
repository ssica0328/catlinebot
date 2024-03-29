# Generated by Django 4.1.3 on 2022-11-23 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='random_exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default='')),
                ('question', models.CharField(blank=True, default=0, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User_Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(default='', max_length=50)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('pic_url', models.CharField(max_length=255)),
                ('mtext', models.CharField(blank=True, max_length=255)),
                ('mdt', models.DateTimeField(auto_now=True)),
                ('points', models.IntegerField(default=0)),
            ],
        ),
    ]
