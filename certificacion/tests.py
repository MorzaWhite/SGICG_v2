from django.test import TestCase
from django.utils import timezone
from .models import Orden, Item, TipoJoya, MaterialJoya
from .services import item_service

class ItemServiceTest(TestCase):

    def setUp(self):
        """Set up a test order and other necessary data."""
        self.orden = Orden.objects.create(
            numero_orden="TEST-001",
            fecha_creacion=timezone.now(),
            fecha_entrega_sugerida=timezone.now()
        )
        self.tipo_joya = TipoJoya.objects.create(nombre="Anillo")
        self.material_joya = MaterialJoya.objects.create(nombre="Oro")

    def test_create_item_successfully(self):
        """Test that an item can be created successfully."""
        item_data = {
            "tipo_certificado": "Gem Card",
            "tipo_item": "Joya",
            "tipo_joya": self.tipo_joya,
            "material_joya": self.material_joya,
            "color_gema": "Azul",
            "peso": 1.5
        }
        item = item_service.save_item(self.orden, item_data)
        self.assertEqual(item.peso, 1.5)
        self.assertEqual(self.orden.items.count(), 1)

    def test_update_item_successfully(self):
        """Test that an item can be updated successfully."""
        item = Item.objects.create(
            orden=self.orden,
            tipo_certificado="Gem Card",
            tipo_item="Joya",
            tipo_joya=self.tipo_joya,
            material_joya=self.material_joya,
            color_gema="Azul",
            peso=1.0
        )
        update_data = {
            "tipo_item": "Joya",
            "tipo_joya": self.tipo_joya,
            "material_joya": self.material_joya,
            "color_gema": "Azul",
            "peso": 2.0
        }
        item_service.update_item(item, update_data)
        item.refresh_from_db()
        self.assertEqual(item.peso, 2.0)

    def test_delivery_date_recalculation(self):
        """Test that the delivery date is recalculated when an item is added."""
        initial_date = self.orden.fecha_entrega_sugerida
        item_data = {
            "tipo_certificado": "Escrito",
            "tipo_item": "Lote de gemas",
            "tipo_gema": "Diamante",
            "cantidad_total": 10,
            "peso_promedio": 0.5
        }
        item_service.save_item(self.orden, item_data)
        self.orden.refresh_from_db()
        self.assertNotEqual(self.orden.fecha_entrega_sugerida, initial_date)
