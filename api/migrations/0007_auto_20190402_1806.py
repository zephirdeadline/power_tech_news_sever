# Generated by Django 2.2 on 2019-04-02 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20190402_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='date',
            field=models.CharField(default='fre', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rss',
            name='date',
            field=models.CharField(default='fred', max_length=128),
            preserve_default=False,
        ),
    ]
