# Generated by Django 2.0.2 on 2018-03-20 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0010_remove_hypothesis_para_list'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question_edit',
            name='para_chains',
        ),
    ]
