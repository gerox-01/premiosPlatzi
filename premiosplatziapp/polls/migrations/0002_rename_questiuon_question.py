# Generated by Django 4.0.1 on 2022-01-22 22:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Questiuon',
            new_name='Question',
        ),
    ]