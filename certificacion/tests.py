from django.test import TestCase, LiveServerTestCase
from django.utils import timezone
from django.contrib.auth.models import User
from playwright.sync_api import sync_playwright
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

class ItemCreationUITest(LiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.orden = Orden.objects.create(numero_orden="UI-TEST-001", fecha_creacion=timezone.now(), fecha_entrega_sugerida=timezone.now())

    def test_add_item_via_ajax_modal(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()

            page.on("console", lambda msg: print(msg.text))

            # Log in
            page.goto(self.live_server_url + '/admin/login/')
            page.fill('input[name=username]', 'testuser')
            page.fill('input[name=password]', 'password')
            page.click('input[type=submit]')

            # Navigate to item creation page
            page.goto(f"{self.live_server_url}/orden/{self.orden.id}/item/nuevo/")
            print(page.content())
            page.pause()

            # Open modal and fill form
            page.click("text=Agregar Item")
            page.select_option("select[name='tipo_certificado']", "Verbal")
            page.select_option("select[name='tipo_item']", "Piedras sueltas")
            page.fill("input[name='color_gema']", "Rojo")
            page.fill("input[name='peso']", "1.0")
            page.fill("input[name='cantidad']", "1")

            # Submit form and check for toast
            page.click("text=Guardar Item")
            self.assertTrue(page.locator("text=✅ Item guardado correctamente").is_visible())

            # Check if item counter updated
            self.assertTrue(page.locator("text=Items Agregados: 1").is_visible())

            browser.close()
