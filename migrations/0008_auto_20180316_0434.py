# Generated by Django 2.0.2 on 2018-03-16 04:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0007_auto_20180315_0924'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question_template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hardness', models.DecimalField(decimal_places=2, max_digits=5)),
                ('edited', models.BooleanField(default=False)),
                ('template', models.TextField()),
                ('question_upload', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='editor.Question_upload')),
            ],
        ),
        migrations.RenameModel(
            old_name='Parameter',
            new_name='Question_edit',
        ),
    ]
