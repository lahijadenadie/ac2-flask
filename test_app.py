import unittest

from app import Usuario, app

class PruebasApp(unittest.TestCase):
    def setUp(self):
        app.config["WTF_CSRF_ENABLED"] = False
        self.cliente = app.test_client()

    def test_modelo_usuario(self):
        usuario = Usuario(nombre="Ana", correo="ana@ejemplo.com")
        self.assertEqual(usuario.nombre, "Ana")
        self.assertEqual(usuario.correo, "ana@ejemplo.com")

    def test_pagina_principal(self):
        respuesta = self.cliente.get("/")
        self.assertEqual(respuesta.status_code, 200)

    def test_pagina_inexistentes(self):
        respuesta = self.cliente.get("/no-existe")
        self.assertEqual(respuesta.status_code, 404)

    def test_formulario_vacio(self):
        respuesta = self.cliente.post("/contacto", data={})
        texto = respuesta.get_data(as_text=True)
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("Escribe tu nombre", texto)

    def test_correo_invalido(self):
        datos = {"nombre": "Ana", "correo": "esto-no-es-un-correo"}
        respuesta = self.cliente.post("/contacto", data=datos)
        texto = respuesta.get_data(as_text=True)
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("Introduce un correo válido, por ejemplo ana@correo.com", texto)

if __name__ == "__main__":
    unittest.main()