# Generated by Django 2.2.7 on 2019-12-21 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tapp', '0009_auto_20191221_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drawquestion',
            name='question_file',
            field=models.FileField(default='Files/empty.json', upload_to='Files/DrawInput/'),
        ),
    ]