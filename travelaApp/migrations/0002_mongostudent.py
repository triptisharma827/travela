# Generated by Django 4.2.1 on 2024-03-15 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travelaApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MongoStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('adhar_number', models.CharField(max_length=12)),
                ('contact_no', models.CharField(max_length=15)),
            ],
        ),
    ]
