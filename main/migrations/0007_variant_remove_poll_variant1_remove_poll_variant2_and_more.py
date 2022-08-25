# Generated by Django 4.1 on 2022-08-21 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_pollresult_product_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='poll',
            name='variant1',
        ),
        migrations.RemoveField(
            model_name='poll',
            name='variant2',
        ),
        migrations.RemoveField(
            model_name='poll',
            name='variant3',
        ),
        migrations.RemoveField(
            model_name='poll',
            name='variant4',
        ),
        migrations.RemoveField(
            model_name='poll',
            name='variant5',
        ),
        migrations.AddField(
            model_name='poll',
            name='variant',
            field=models.ManyToManyField(blank=True, to='main.variant'),
        ),
    ]