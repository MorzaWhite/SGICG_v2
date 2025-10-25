
import re
import time
from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    def get_preview_field(name):
        return page.locator(f"#preview-panel [data-preview='{name}']")

    try:
        # 1. Create a new order with manual order number
        page.goto("http://127.0.0.1:8000/orden/nueva/")
        order_number = f"ORD-{int(time.time())}"
        page.fill("input[name='numero_orden']", order_number)
        page.fill("textarea[name='tags']", "Initial Tags")
        page.click("button[type='submit']")

        # 2. Verify redirection to item form and check initial preview
        expect(page).to_have_url(re.compile(r"/orden/\d+/item/nuevo/"))
        expect(get_preview_field('tags')).to_contain_text("Initial Tags")
        page.screenshot(path="jules-scratch/verification/01_item_form_loaded.png")

        # 3. Test dynamic fields for 'Joya' and 'Topos' insurance
        page.select_option("select[name='tipo_item']", "Joya")
        page.select_option("select[name='tipo_joya']", "Topos")
        expect(page.locator("#seguro-field")).to_be_visible()
        page.check("input[name='tiene_seguro']")

        # Verify preview updates
        expect(get_preview_field('tipo_item')).to_contain_text("Joya")
        expect(get_preview_field('tipo_joya')).to_contain_text("Topos")
        expect(get_preview_field('tiene_seguro')).to_contain_text("Sí")
        page.screenshot(path="jules-scratch/verification/02_topos_insurance_visible.png")

        # 4. Test form reset
        page.click("button#reset-button")
        expect(page.locator("#seguro-field")).to_be_hidden()
        expect(get_preview_field('tipo_joya')).not_to_be_visible()
        page.screenshot(path="jules-scratch/verification/03_form_reset.png")

        # 5. Fill and submit a valid item
        page.select_option("select[name='tipo_certificado']", "Gem Card")
        page.select_option("select[name='tipo_item']", "Piedras sueltas")
        page.fill("input[name='color_gema']", "Esmeralda")
        page.fill("input[name='peso']", "2.1")
        page.fill("input[name='cantidad']", "1")
        page.click("button[type='submit']")

        # 6. Verify success message and clean form for next item
        expect(page.locator("text=/Item agregado correctamente/")).to_be_visible()
        expect(page.locator("input[name='color_gema']")).to_have_value("")
        page.screenshot(path="jules-scratch/verification/04_submission_success.png")

    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
