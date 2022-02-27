# Generated by Django 3.2.12 on 2022-02-26 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('email', models.CharField(max_length=100)),
                ('query', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('roll_no', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=100)),
                ('hostel', models.CharField(max_length=5)),
                ('room_no', models.CharField(max_length=7)),
                ('image', models.ImageField(upload_to='attendance/images/')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=1)),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.date')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.student')),
            ],
        ),
    ]
