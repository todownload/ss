# Generated by Django 2.2.7 on 2019-12-21 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tapp', '0011_auto_20191221_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drawquestion',
            name='question_image',
            field=models.ImageField(default='Files/Img/green_bg.png', upload_to='Tapp/static/Tapp/images/Draw'),
        ),
    ]