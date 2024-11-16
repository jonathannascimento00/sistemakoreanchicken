# Generated by Django 4.2.16 on 2024-11-13 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_usuario_is_temporary_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='perfil',
            field=models.CharField(choices=[('ADMIN', 'Administrador'), ('COLAB', 'Colaborador')], default='COLAB', max_length=6),
        ),
    ]