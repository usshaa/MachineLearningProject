# Generated by Django 4.1.7 on 2023-03-13 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=255)),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('month', models.IntegerField()),
                ('city', models.CharField(max_length=255)),
                ('hour', models.IntegerField()),
                ('prediction', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
