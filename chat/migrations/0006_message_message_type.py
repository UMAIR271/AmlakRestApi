# Generated by Django 4.1 on 2022-11-05 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_chat_inbox_socket_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='message_type',
            field=models.CharField(max_length=1200, null=True),
        ),
    ]
