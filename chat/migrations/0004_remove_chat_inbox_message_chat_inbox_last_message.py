# Generated by Django 4.1 on 2022-11-04 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_message_socket_id_chat_inbox'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat_inbox',
            name='message',
        ),
        migrations.AddField(
            model_name='chat_inbox',
            name='last_message',
            field=models.CharField(max_length=1200, null=True),
        ),
    ]
