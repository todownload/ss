# Generated by Django 2.2.7 on 2019-12-20 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tapp', '0005_auto_20191220_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='designquestion',
            name='question_title',
            field=models.CharField(default='Question', max_length=20),
        ),
        migrations.AddField(
            model_name='drawquestion',
            name='question_title',
            field=models.CharField(default='Question', max_length=20),
        ),
        migrations.AddField(
            model_name='selectquestion',
            name='question_title',
            field=models.CharField(default='Question', max_length=20),
        ),
    ]