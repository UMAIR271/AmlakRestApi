# Generated by Django 4.1 on 2022-09-20 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0002_remove_listing_property_usage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='property_usage',
            field=models.CharField(choices=[('Single Family', 'Single Family'), ('Bachelors', 'Bachelors')], max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='Furnishing_type',
            field=models.CharField(choices=[('Unfurnished', 'Unfurnished'), ('Semi-furnished', 'Semi-furnished'), ('Furnished', 'Furnished')], max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='Property_Tenure',
            field=models.CharField(choices=[('FreeHold', 'FreeHold'), ('Non FreeHold', 'Non FreeHold'), ('LeaseHold', 'LeaseHold')], max_length=13, null=True),
        ),
    ]
