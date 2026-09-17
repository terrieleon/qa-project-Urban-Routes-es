from time import sleep

from PIL.ImImagePlugin import number

import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    button_reservar = (By.XPATH, '//button[@class="button round"]')
    tarifa_comfort = (By.XPATH, "//div[text()='Comfort' and @class='tcard-title']")
    seleccionar_telefono =  (By.XPATH, "//div[text()='Número de teléfono' and @class='np-text']")
    rellenar_numero_telefono = (By.ID, 'phone')
    button_siguiente = (By.XPATH, "//div[@class='number-picker open']//button[text()='Siguiente']")
    codigo_telefono = (By.XPATH, "//div[@class='number-picker open']//input[@id='code']")
    confirmar = (By.XPATH, "//div[@class='number-picker open']//button[text()='Confirmar']")
    metodo = (By.XPATH, "//div[text()='Método de pago' and @class='pp-text']")
    agregar_tarjeta = (By.XPATH, "//div[text()='Agregar tarjeta' and @class='pp-title']")
    numero_tarjeta = (By.ID, 'number')
    codigo = (By.XPATH, "//div[@class='payment-picker open']//input[@id='code']")
    boton_agregar = (By.XPATH, "//button[text()='Agregar']")
    cerrar_pagamento = (By.XPATH, "//div[@class='payment-picker open']//button[@class='close-button section-close']")
    campo_mensaje = (By.ID, 'comment')
    pedir_manta = (By.XPATH, "(//div[@class='tariff-picker shown']//span[@class= 'slider round'])[1]")
    pedir_helado = (By.XPATH, "(//div[@class='r-counter-container']//div[@class='counter-plus'])[1]")
    boton_pedir_taxi = (By.XPATH, "//div[@class='workflow']/div[@class='smart-button-wrapper']/button[@class='smart-button']")
    modal = (By.XPATH, "//div[@class='order shown']")


    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.from_field))
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def clic_button_reservar(self):
        button_reservar = WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.button_reservar))
        button_reservar.click()

    def seleccionar_tarifa_comfort(self):
        tarifa_comfort = WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.tarifa_comfort))
        tarifa_comfort.click()

    def seleccionar_campo_telefono(self):
        self.driver.find_element(*self.seleccionar_telefono).click()

    def rellenar_numero_telefono2 (self, number):
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.rellenar_numero_telefono))
        self.driver.find_element(*self.rellenar_numero_telefono).send_keys(number)

    def clic_boton_siguiente(self):
        boton_siguiente = WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.button_siguiente))
        boton_siguiente.click()

    def rellenar_codigo_telef(self,number):
        codigo_telefono_field = WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.codigo_telefono))
        codigo_telefono_field.send_keys(number)

    def clic_confirmar(self):
        self.driver.find_element(*self.confirmar).click()

    def metodo_de_pago(self):
        self.driver.find_element(*self.metodo).click()

    def clic_agregar_tarjeta(self):
        agregar_tarjeta= WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.agregar_tarjeta))
        agregar_tarjeta.click()

    def rellenar_numero_tarjeta(self, number):
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.numero_tarjeta))
        self.driver.find_element(*self.numero_tarjeta).send_keys(number)

    def rellenar_codigo(self, number):
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.codigo))
        self.driver.find_element(*self.codigo).send_keys(number+Keys.TAB)

    def clic_boton_agregar(self):
        boton_agregar=WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.boton_agregar))
        boton_agregar.click()

    def clic_cerrar(self):
        cerrar=WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.cerrar_pagamento))
        cerrar.click()

    def mensaje_para_el_conductor(self,mensaje):
        self.driver.find_element(*self.campo_mensaje).send_keys(mensaje)

    def pedir_manta_y_pañuelos (self):
        self.driver.find_element(*self.pedir_manta).click()

    def pedir_helados (self):
        pedir_helado1= self.driver.find_element(*self.pedir_helado)
        pedir_helado1.click()
        pedir_helado1.click()

    def click_pedir_taxi(self):
        pedir_taxi = WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.boton_pedir_taxi))
        pedir_taxi.click()

    def check_modal(self):
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.modal))


class TestUrbanRoutes:

   driver = None

    def setup_method(self):
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        self.driver = webdriver.Chrome(service=Service(), options=options)
        self.driver.get(data.urban_routes_url)
        self.routes_page = UrbanRoutesPage(self.driver)


    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_verificar_button_reservar(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.clic_button_reservar()

    def test_seleccionar_tarifa_comfort(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.seleccionar_tarifa_comfort()

    def test_rellenar_numero_telefono (self):
        routes_page = UrbanRoutesPage(self.driver)
        phone=data.phone_number
        routes_page.seleccionar_campo_telefono()
        routes_page.rellenar_numero_telefono2(phone)
        routes_page.clic_boton_siguiente()
        code = retrieve_phone_code(self.driver)
        routes_page.rellenar_codigo_telef(code)
        routes_page.clic_confirmar()

    def test_agregar_numerotarjeta (self):
        routes_page = UrbanRoutesPage(self.driver)
        tarjeta=data.card_number
        codigo=data.card_code
        routes_page.metodo_de_pago()
        routes_page.clic_agregar_tarjeta()
        routes_page.rellenar_numero_tarjeta(tarjeta)
        routes_page.rellenar_codigo(codigo)
        routes_page.clic_boton_agregar()
        routes_page.clic_cerrar()

    def test_compila_campo_mensaje (self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.mensaje_para_el_conductor(data.message_for_driver)

    def test_ordenar_manta (self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.pedir_manta_y_pañuelos()

    def test_ordenar_helados (self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.pedir_helados()

    def test_pedir_taxi(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_pedir_taxi()
        routes_page.check_modal()

   def teardown_method(self):
    if self.driver is not None:
        self.driver.quit()