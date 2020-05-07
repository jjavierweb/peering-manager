# Generated by Django 3.0.5 on 2020-04-27 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("peering", "0056_autonomoussystem_prefixes"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="community",
            options={
                "ordering": ["value", "name", "description"],
                "verbose_name_plural": "communities",
            },
        ),
        migrations.AddField(
            model_name="community",
            name="description",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
