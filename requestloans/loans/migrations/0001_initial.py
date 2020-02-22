# Generated by Django 3.0.3 on 2020-02-22 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('dni', models.CharField(max_length=8)),
                ('firstname', models.CharField(max_length=150)),
                ('lastname', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('A', 'Another')], max_length=1)),
                ('email', models.EmailField(help_text='Example: pepe@localhost', max_length=250)),
                ('approved', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'loans',
                'ordering': ('id',),
            },
        ),
    ]