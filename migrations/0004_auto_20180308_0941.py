# Generated by Django 2.0.2 on 2018-03-08 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0003_auto_20180306_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question_upload',
            name='types',
            field=models.CharField(choices=[('算数または方程式', '方程式'), ('条件つき問題', '条件つき問題')], default='算数または方程式', max_length=40),
        ),
    ]
