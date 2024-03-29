# Generated by Django 4.1.3 on 2022-11-29 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cat_linebot', '0005_乖乖吃飯_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='pidan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=0)),
                ('name', models.CharField(blank=True, default='', max_length=255)),
                ('price', models.CharField(blank=True, default='', max_length=255)),
                ('grams', models.CharField(blank=True, default='', max_length=255)),
                ('material', models.CharField(blank=True, default='', max_length=255)),
                ('ratio', models.CharField(blank=True, default='', max_length=255)),
                ('score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='心靈雞湯',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=0)),
                ('name', models.CharField(blank=True, default='', max_length=255)),
                ('price', models.CharField(blank=True, default='', max_length=255)),
                ('grams', models.CharField(blank=True, default='', max_length=255)),
                ('protein', models.CharField(blank=True, default='', max_length=255)),
                ('fat', models.CharField(blank=True, default='', max_length=255)),
                ('carbo', models.CharField(blank=True, default='', max_length=255)),
                ('phos', models.CharField(blank=True, default='', max_length=255)),
                ('kcal', models.CharField(blank=True, default='', max_length=255)),
                ('score', models.IntegerField(default=0)),
            ],
        ),
        migrations.RenameField(
            model_name='乖乖吃飯',
            old_name='grans',
            new_name='grams',
        ),
    ]
