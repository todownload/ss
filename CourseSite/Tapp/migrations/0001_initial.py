# Generated by Django 2.2.7 on 2019-12-10 01:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=50)),
                ('course_id', models.CharField(max_length=20, unique=True)),
                ('course_starttime', models.DateTimeField(verbose_name='start time')),
                ('course_endtime', models.DateTimeField(verbose_name='end time')),
                ('course_stu_num', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Knowledge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('knowledge_name', models.CharField(max_length=30, unique=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tapp.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stu_name', models.CharField(max_length=20)),
                ('stu_id', models.CharField(max_length=15, unique=True)),
                ('stu_pwd', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_name', models.CharField(max_length=20)),
                ('teacher_id', models.CharField(max_length=15, unique=True)),
                ('teacher_pwd', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='SelectQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('total_submit', models.IntegerField(default=0)),
                ('correct_submit', models.IntegerField(default=0)),
                ('answer', models.CharField(choices=[('A', 'Answer A'), ('B', 'Answer B'), ('C', 'Answer C'), ('D', 'Answer D')], max_length=1)),
                ('choice_A', models.CharField(max_length=100)),
                ('choice_B', models.CharField(max_length=100)),
                ('choice_C', models.CharField(max_length=100)),
                ('choice_D', models.CharField(max_length=100)),
                ('question_analysis', models.TextField(default='')),
                ('knowledge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tapp.Knowledge')),
            ],
        ),
        migrations.CreateModel(
            name='DrawQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('total_submit', models.IntegerField(default=0)),
                ('correct_submit', models.IntegerField(default=0)),
                ('knowledge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tapp.Knowledge')),
            ],
        ),
        migrations.CreateModel(
            name='DesignQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('question_language', models.CharField(max_length=30)),
                ('total_submit', models.IntegerField(default=0)),
                ('correct_submit', models.IntegerField(default=0)),
                ('example_input', models.CharField(max_length=100)),
                ('example_output', models.CharField(max_length=100)),
                ('question_analysis', models.TextField(default='')),
                ('knowledge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tapp.Knowledge')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(to='Tapp.Student'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tapp.Teacher'),
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anno_title', models.CharField(max_length=50)),
                ('anno_content', models.TextField(default='')),
                ('anno_pubtime', models.DateTimeField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tapp.Course')),
            ],
        ),
    ]