# Generated by Django 4.1.3 on 2022-11-23 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cat_linebot', '0002_alter_random_exam_num_alter_random_exam_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='random_exam',
            name='ans',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='random_exam',
            name='op1',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='random_exam',
            name='op2',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='random_exam',
            name='op3',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]