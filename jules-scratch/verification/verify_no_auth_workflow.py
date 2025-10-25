
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
        order_number = f"ORD-NOAUTH-{int(time.time())}"
        page.fill("input[name='numero_orden']", order_number)
        page.click("button[type='submit']")
        expect(page).to_have_url(re.compile(r"/orden/\d+/item/nuevo/"))

        # 2. Open modal and add a 'Piedras sueltas' item
        page.click("text=Agregar Item")
        expect(page.locator("h2:has-text('Agregar Nuevo Item')")).to_be_visible()

        page.select_option("select[name='tipo_certificado']", "Verbal")
        page.select_option("select[name='tipo_item']", "Piedras sueltas")
        page.fill("input[name='color_gema']", "Azul")
        page.fill("input[name='peso']", "1.0")
        page.fill("input[name='cantidad']", "1")

        page.click("text=Guardar Item")

        # 3. Verify item appears in the list and toast is shown
        expect(page.locator("text=✅ Item guardado correctamente")).to_be_visible()
        expect(page.locator("#item-list div:has-text('Piedras sueltas')")).to_be_visible()
        expect(page.locator("h2:has-text('Items Agregados: 1')")).to_be_visible()
        page.screenshot(path="jules-scratch/verification/no_auth_workflow.png")

    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
