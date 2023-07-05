# Generated by Django 4.2.2 on 2023-07-05 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('puntos', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Deporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(default='', help_text='Codigo Corto', max_length=5)),
                ('nombre', models.CharField(help_text='Descripcion', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('puntos', models.IntegerField(default=0)),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='colores', to='core.color')),
            ],
        ),
        migrations.CreateModel(
            name='Torneo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Jugador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='color_jugador', to='core.color')),
                ('equipo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jugadores', to='core.equipo')),
            ],
        ),
        migrations.AddField(
            model_name='equipo',
            name='torneo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipos', to='core.torneo'),
        ),
        migrations.CreateModel(
            name='Encuentro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(blank=True, null=True)),
                ('lugar', models.CharField(blank=True, max_length=100)),
                ('resultado_local', models.PositiveIntegerField(blank=True, null=True)),
                ('resultado_visitante', models.PositiveIntegerField(blank=True, null=True)),
                ('puntos_ganador', models.IntegerField(default=3, help_text='Define los puntos otorgados al ganador')),
                ('puntos_empate', models.IntegerField(default=1, help_text='Define los puntos otorgados el empate')),
                ('finalizado', models.BooleanField(default=False)),
                ('deporte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.deporte')),
                ('equipo_ganador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='encuentros_e_ganados', to='core.equipo')),
                ('equipo_local', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='encuentros_locales', to='core.equipo')),
                ('equipo_visitante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='encuentros_visitantes', to='core.equipo')),
                ('judador_visitante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='encuentros_visitantes', to='core.jugador')),
                ('jugador_ganador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='encuentros_j_ganados', to='core.equipo')),
                ('jugador_local', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='encuentros_locales', to='core.jugador')),
                ('torneo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.torneo')),
            ],
        ),
        migrations.AddField(
            model_name='deporte',
            name='torneo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.torneo'),
        ),
        migrations.CreateModel(
            name='ColorDeportePuntos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntos', models.IntegerField(default=0)),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='color', to='core.color')),
                ('deporte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.deporte')),
                ('torneo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.torneo')),
            ],
        ),
        migrations.AddField(
            model_name='color',
            name='torneo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.torneo'),
        ),
    ]
