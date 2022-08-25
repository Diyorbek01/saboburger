# Generated by Django 4.1 on 2022-08-20 03:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_offer_user_category_pollresult'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pollresult',
            name='product_category',
        ),
        migrations.RemoveField(
            model_name='pollresult',
            name='question',
        ),
        migrations.RemoveField(
            model_name='pollresult',
            name='staff_category',
        ),
        migrations.AddField(
            model_name='pollresult',
            name='poll',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.poll'),
        ),
    ]