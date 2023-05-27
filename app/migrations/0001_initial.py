# Generated by Django 4.1.5 on 2023-01-31 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "id",
                    models.CharField(max_length=10, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=50)),
                ("email", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Detected",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("time_stamp", models.DateTimeField()),
                (
                    "photo",
                    models.ImageField(
                        default="app/facerec/detected/noimg.png", upload_to="detected/"
                    ),
                ),
                (
                    "emp_id",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.employee",
                    ),
                ),
            ],
        ),
    ]
