# Generated by Django 4.1 on 2022-11-05 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_alter_chat_inbox_socket_id_alter_message_socket_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat_inbox',
            name='socket_id',
            field=models.UUIDField(null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='socket_id',
            field=models.UUIDField(null=True),
        ),
    ]
