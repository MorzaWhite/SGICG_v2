from django.db import migrations

def add_topos_joya(apps, schema_editor):
    TipoJoya = apps.get_model('certificacion', 'TipoJoya')
    TipoJoya.objects.create(nombre='Topos')

class Migration(migrations.Migration):

    dependencies = [
        ('certificacion', '0004_remove_orden_color_gema_remove_orden_material_joya_and_more'),
    ]

    operations = [
        migrations.RunPython(add_topos_joya),
    ]
