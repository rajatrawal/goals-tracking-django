# Generated by Django 4.2 on 2023-04-29 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='user_goal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goals', to='home.usergoal'),
        ),
    ]
