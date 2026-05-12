
Manejo de excepciones

En testing, las excepciones no son errores del sistema; a menudo son resultados esperados. El SDET debe controlarlas con maestría.

    Excepciones checked vs unchecked: Los frameworks de testing (TestNG, JUnit) capturan cualquier excepción y la convierten en fallo. No es necesario propagarlas siempre; a veces se atrapan para verificar comportamiento esperado:
    java

    Assertions.assertThrows(NoSuchElementException.class, () -> {
        driver.findElement(By.id("inexistente"));
    });

    Try-catch en automatización: Cuando se espera que una operación pueda fallar (por ejemplo, un pop-up que a veces no aparece), se usa try-catch para evitar que la prueba se detenga abruptamente. Pero un abuso genera falsos positivos; se prefiere usar esperas explícitas (WebDriverWait) que lanzan excepciones manejables.

    Excepciones personalizadas: Un SDET puede crear TestDataException, EnvironmentSetupException, AssertionError personalizado con mensajes claros y datos para debugging.

    Logging y manejo en hooks: En frameworks basados en Cucumber o TestNG, los hooks @After capturan excepciones para hacer capturas de pantalla, guardar logs y limpiar el estado.