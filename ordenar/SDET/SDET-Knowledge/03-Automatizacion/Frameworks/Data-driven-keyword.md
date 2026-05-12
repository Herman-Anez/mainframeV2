# Data-driven & Keyword-driven

Son dos enfoques históricos importantes para construir frameworks de automatización.

## Data-driven Testing

Las pruebas obtienen los datos de entrada y resultados esperados desde fuentes externas (Excel, CSV, base de datos), y la misma lógica de prueba se ejecuta para cada fila.

- **Implementación**: Mediante `TestNG DataProvider`, `JUnit 5 Parameterized Tests`, `pytest.parametrize`, etc. El SDET lee el archivo de datos, lo transforma en un iterador y ejecuta el test.
- **Ventaja**: Añadir un nuevo caso es solo añadir una fila de datos sin necesidad de programar.
- **Desafío**: La lógica de prueba debe ser genérica; los datos deben cubrir todas las variantes posibles.

## Keyword-driven Testing

Cada acción se representa como una "palabra clave" (*keyword*) que se mapea a código. Los casos de prueba son secuencias de keywords en una tabla.

### Ejemplo de Estructura

| Keyword | Locator | Value |
| :--- | :--- | :--- |
| `openBrowser` | `Chrome` | |
| `navigate` | `https://example.com` | |
| `input` | `id=user` | `admin` |
| `click` | `id=login` | |
| `verifyText` | `id=welcome` | `Bienvenido` |

- **Motor**: Un motor lee la tabla y, mediante *reflection* o un diccionario de comandos, invoca los métodos correspondientes.
- **Herramientas**: **Robot Framework** es el exponente más conocido.

> [!NOTE]
> El SDET actual suele evitar construir un motor *keyword-driven* desde cero debido a que las capas de abstracción modernas (Screenplay, BDD) ofrecen mejor mantenibilidad. Sin embargo, Robot Framework es apropiado en entornos donde los testers no programan.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Cucumber & BDD](./Cucumber-BDD.md) | [Home](../../index.md) | [Módulo Siguiente](../../04-CI-CD/index.md) |

