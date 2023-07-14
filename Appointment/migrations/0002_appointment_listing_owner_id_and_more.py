# Generated by Django 4.0.5 on 2022-11-29 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0008_remove_listing_is_favourite'),
        ('Appointment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='Listing_Owner_Id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ListingOwnerId', to='listing.listing'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='listing_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ListingId', to='listing.listing'),
        ),
    ]
