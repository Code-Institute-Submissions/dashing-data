# Generated by Django 3.0.3 on 2020-03-04 22:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BarChart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_data', models.CharField(max_length=50)),
                ('y_data', models.DecimalField(decimal_places=5, max_digits=14)),
                ('chart_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.UserChart')),
            ],
        ),
    ]