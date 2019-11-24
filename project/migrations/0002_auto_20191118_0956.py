# Generated by Django 2.1.4 on 2019-11-18 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='issuecomments',
            name='issue',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='project.Issue'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taskcomments',
            name='task',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='project.Task'),
            preserve_default=False,
        ),
    ]