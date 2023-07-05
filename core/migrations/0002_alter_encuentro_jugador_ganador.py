# Generated by Django 4.2.2 on 2023-07-05 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encuentro',
            name='jugador_ganador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='encuentros_j_ganados', to='core.jugador'),
        ),
    ]