
Bibliotecas de testing esenciales en Python

    requests + pytest: Automatización de API. Se usa requests para HTTP y pytest para estructurar pruebas. Se combinan fixtures para autenticación (obtener token) y parámetros.
    python

    def test_get_user(api_base_url, auth_token):
        resp = requests.get(f"{api_base_url}/users/1", headers={"Authorization": f"Bearer {auth_token}"})
        assert resp.status_code == 200
        assert resp.json()["name"] == "Juan"

    Selenium / Playwright con pytest: Se usan fixtures para el navegador. Playwright suele ser la opción moderna por su velocidad y trazabilidad.

    Mocking con unittest.mock: Para simular respuestas de bases de datos o servicios externos sin depender de ellos. patch reemplaza objetos durante una prueba.

    Factory Boy: Crea instancias de objetos (modelos de base de datos, datos de entrada) con valores aleatorios o predefinidos, ideal para data-driven testing.

    Faker: Genera datos realistas (nombres, emails, direcciones) para pruebas. Se combina con Factory Boy.

    Cobertura: pytest-cov mide cobertura de código. El SDET lo integra en CI para establecer umbrales (p.ej., 80% de líneas).