# Generated by Django 4.1.3 on 2022-11-28 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cat_linebot', '0003_random_exam_ans_random_exam_op1_random_exam_op2_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='乖乖吃飯',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=0)),
                ('price', models.CharField(blank=True, default='', max_length=255)),
                ('grans', models.CharField(blank=True, default='', max_length=255)),
                ('protein', models.CharField(blank=True, default='', max_length=255)),
                ('fat', models.CharField(blank=True, default='', max_length=255)),
                ('carbo', models.CharField(blank=True, default='', max_length=255)),
                ('phos', models.CharField(blank=True, default='', max_length=255)),
                ('kcal', models.CharField(blank=True, default='', max_length=255)),
                ('score', models.IntegerField(default=0)),
            ],
        ),
    ]
