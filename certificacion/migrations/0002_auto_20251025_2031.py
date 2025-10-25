from django.db import migrations

def populate_initial_data(apps, schema_editor):
    TipoJoya = apps.get_model('certificacion', 'TipoJoya')
    MaterialJoya = apps.get_model('certificacion', 'MaterialJoya')

    TipoJoya.objects.bulk_create([
        TipoJoya(nombre='Anillo'),
        TipoJoya(nombre='Collar'),
        TipoJoya(nombre='Pulsera'),
        TipoJoya(nombre='Aretes'),
        TipoJoya(nombre='No especificado'),
    ])

    MaterialJoya.objects.bulk_create([
        MaterialJoya(nombre='Oro'),
        MaterialJoya(nombre='Plata'),
        MaterialJoya(nombre='Platino'),
        MaterialJoya(nombre='No especificado'),
    ])

class Migration(migrations.Migration):

    dependencies = [
        ('certificacion', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_initial_data),
    ]
