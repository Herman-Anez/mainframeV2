Data-driven y Keyword-driven

Son dos enfoques históricos importantes para construir frameworks de automatización.

Data-driven Testing:
Las pruebas obtienen los datos de entrada y resultados esperados desde fuentes externas (Excel, CSV, base de datos), y la misma lógica de prueba se ejecuta para cada fila.

    Implementación: con TestNG DataProvider, JUnit5 parametrized tests, pytest parametrize, etc. El SDET lee el archivo de datos, lo transforma en un iterador y ejecuta.

    Ventaja: añadir un nuevo caso es solo añadir una fila sin programar.

    Desafío: la lógica de prueba debe ser suficientemente genérica; los datos deben cubrir todas las variantes.

Keyword-driven Testing:
Cada acción se representa como una "palabra clave" (keyword) que se mapea a código. Los casos de prueba son secuencias de keywords en una tabla.

    Ejemplo de tabla Excel:
    Keyword	Locator	Value
    openBrowser	Chrome	
    navigate	https://...	
    input	id=user	admin
    click	id=login	
    verifyText	id=welcome	Bienvenido

    Un motor lee la tabla y mediante reflection o diccionario invoca los métodos correspondientes.

    Herramientas: Robot Framework es el exponente más conocido. Selenium IDE también genera keywords.

    El SDET actual suele evitar construir un motor keyword-driven desde cero porque las capas de abstracción modernas (Screenplay, BDD) ofrecen mejor mantenibilidad; sin embargo, Robot Framework es apropiado en entornos donde los testers no programan pero necesitan automatizar.

Conclusión:
Para un SDET, los frameworks de ejecución (JUnit/TestNG) y el patrón BDD/Cucumber son herramientas diarias. Las técnicas data-driven forman parte natural de la parametrización, mientras que keyword-driven se reserva para contextos muy específicos con herramientas como Robot Framework.
