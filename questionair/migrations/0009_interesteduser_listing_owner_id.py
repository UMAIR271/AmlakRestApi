# Generated by Django 4.1 on 2022-11-14 18:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questionair', '0008_interesteduser_match_ans'),
    ]

    operations = [
        migrations.AddField(
            model_name='interesteduser',
            name='listing_owner_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing_owner_id', to=settings.AUTH_USER_MODEL),
        ),
    ]
