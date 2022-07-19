# Generated by Django 3.2 on 2022-07-19 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=64)),
                ('amount', models.IntegerField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('description', models.TextField()),
                ('price', models.PositiveBigIntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='category.category')),
            ],
        ),
    ]
