# Generated by Django 4.2.1 on 2023-05-19 14:44

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Rate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("vendor", models.CharField(max_length=255)),
                ("currency_a", models.CharField(max_length=3)),
                ("currency_b", models.CharField(max_length=3)),
                ("sell", models.DecimalField(decimal_places=5, max_digits=10)),
                ("buy", models.DecimalField(decimal_places=5, max_digits=10)),
            ],
        ),
        migrations.AddConstraint(
            model_name="rate",
            constraint=models.UniqueConstraint(
                fields=("date", "vendor", "currency_a", "currency_b"),
                name="unique_rate",
            ),
        ),
    ]