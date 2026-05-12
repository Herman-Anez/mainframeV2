# Fundamentos de Pytest

`pytest` es más que un runner; es un framework extensible mediante plugins y *fixtures*.

## Conceptos principales

*   **Instalación y ejecución**: `pip install pytest`. Ejecutar con `pytest tests/`. Descubre automáticamente archivos `test_*.py` y funciones `test_*`.
*   **Fixtures**: Son el sustituto de `@Before`/`@After`. Proporcionan datos preconfigurados y estado compartido con una limpieza segura. El *scope* puede ser `function` (por defecto), `class`, `module` o `session`.
    ```python
    @pytest.fixture(scope="function")
    def driver():
        driver = webdriver.Chrome()
        yield driver
        driver.quit()
    ```
*   **Parametrización**: Permite ejecutar la misma prueba con diferentes conjuntos de datos usando el decorador `@pytest.mark.parametrize`. Esto elimina la necesidad de bucles manuales y genera reportes individuales para cada caso.
    ```python
    @pytest.mark.parametrize("username,password,expected", [
        ("user1", "pass1", 200),
        ("user2", "wrong", 401),
    ])
    def test_login(username, password, expected):
        response = login_api(username, password)
        assert response.status_code == expected
    ```
*   **Marks (marcadores)**: Clasifican pruebas: `@pytest.mark.smoke`, `@pytest.mark.regression`. Se filtran por marcador: `pytest -m smoke`.
*   **Hooks y conftest.py**: Los archivos `conftest.py` definen fixtures a nivel de directorio y se comparten automáticamente. Los *hooks* permiten modificar el comportamiento de `pytest` (ej. capturar pantalla en fallo).
*   **Asserts avanzados**: `pytest` reescribe las aserciones para mostrar valores en fallo sin necesidad de `assertEqual`. Admite `assert a == b`, `assert result in list`, `pytest.raises`.

---

| Anterior | Inicio | Siguiente |
| :------- | :----: | :-------- |
| ⏪ [Python para SDET](index.md) | [Índice](index.md) | [Bibliotecas de testing](Bibliotecas-testing.md) ⏩ |
