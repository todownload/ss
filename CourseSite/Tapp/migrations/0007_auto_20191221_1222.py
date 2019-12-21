# Generated by Django 2.2.7 on 2019-12-21 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tapp', '0006_auto_20191220_2338'),
    ]

    operations = [
        migrations.AddField(
            model_name='drawquestion',
            name='question_file',
            field=models.FileField(default='Files/empty.json', upload_to='Files/DrawInput'),
        ),
        migrations.AddField(
            model_name='drawquestion',
            name='question_image',
            field=models.ImageField(default='Files/Img/green_bg.png', upload_to='static/Tapp/images/'),
        ),
        migrations.AddField(
            model_name='drawquestion',
            name='question_type',
            field=models.IntegerField(choices=[('0', 'Draw Graph'), ('1', 'Fill Table')], default=0, max_length=1),
        ),
    ]