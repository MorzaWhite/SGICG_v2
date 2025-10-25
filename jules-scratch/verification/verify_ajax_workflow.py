
import re
import time
from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        # 1. Create a new order
        page.goto("http://127.0.0.1:8000/orden/nueva/")
        order_number = f"ORD-AJAX-{int(time.time())}"
        page.fill("input[name='numero_orden']", order_number)
        page.click("button[type='submit']")
        expect(page).to_have_url(re.compile(r"/orden/\d+/item/nuevo/"))
        page.screenshot(path="jules-scratch/verification/01_item_page_loaded.png")

        # 2. Open modal and add a 'Piedras sueltas' item
        page.click("text=Agregar Item")
        expect(page.locator("h2:has-text('Agregar Nuevo Item')")).to_be_visible()

        page.select_option("select[name='tipo_certificado']", "Verbal")
        page.select_option("select[name='tipo_item']", "Piedras sueltas")

        # Wait for the dynamic fields to be visible
        page.wait_for_selector(".form-field[data-field-name='color_gema']")

        page.fill("input[name='color_gema']", "Verde")
        page.fill("input[name='peso']", "3.0")
        page.fill("input[name='cantidad']", "4")

        page.click("button[type='submit']:has-text('Guardar Item')")

        # 3. Verify item appears in the list and toast is shown
        expect(page.locator("text=/Item guardado exitosamente/")).to_be_visible()
        expect(page.locator("#item-list div:has-text('Piedras sueltas')")).to_be_visible()
        expect(page.locator("h2:has-text('Items Agregados: 1')")).to_be_visible()
        page.screenshot(path="jules-scratch/verification/02_item_created.png")

        # 4. Edit the item
        page.click("text=Editar")
        expect(page.locator("h2:has-text('Editar Item')")).to_be_visible()
        page.fill("input[name='peso']", "3.5")
        page.click("button[type='submit']:has-text('Actualizar Item')")

        # 5. Verify update
        expect(page.locator("text=/Item guardado exitosamente/")).to_be_visible()
        expect(page.locator("#item-list div:has-text('Peso: 3.5')")).to_be_visible()
        page.screenshot(path="jules-scratch/verification/03_item_edited.png")

    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
