# Generated by Django 2.2 on 2019-04-02 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20190402_0710'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feed',
            name='url_origin',
        ),
    ]