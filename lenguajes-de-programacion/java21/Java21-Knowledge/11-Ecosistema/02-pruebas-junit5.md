# PRUEBAS CON JUNIT 5
1. JUnit 5: la plataforma moderna de testing

JUnit 5 (Jupiter) es el estándar para pruebas unitarias y de integración en Java. Lanzado en 2017, ha ido mejorando cada versión y en Java 21 sigue evolucionando (versión 5.10+). Está compuesto por:

    JUnit Platform: base que permite ejecutar cualquier motor de tests (JUnit Vintage para JUnit 3/4, Jupiter, etc.).

    JUnit Jupiter: nuevo API de programación de tests.

    JUnit Vintage: retrocompatibilidad con JUnit 3/4.

2. Anotaciones y estructura básica de un test
```java
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class CalculadoraTest {
```

### Calculadora calc;

### @BeforeAll
    void initAll() {
        System.out.println("Antes de todos los tests");
    }

### @BeforeEach
    void init() {
        calc = new Calculadora();
    }

### @Test
    @DisplayName("Suma de dos números positivos")
    void testSuma() {
        assertEquals(5, calc.sumar(2, 3), "2+3 debería ser 5");
    }

### @Test
    @Disabled("Funcionalidad aún no implementada")
    void testResta() { }

### @AfterEach
    void tearDown() {
        calc = null;
    }

### @AfterAll
    static void cleanAll() {
        System.out.println("Después de todos los tests");
    }
}

3. Aserciones principales

### assertEquals(expected, actual)

### assertTrue(condition), assertFalse(condition)

### assertNull(obj), assertNotNull(obj)

### assertSame, assertNotSame

    assertThrows(Exception.class, () -> { ... }) → captura y verifica excepciones.

### assertTimeout(Duration.ofMillis(100), () -> { ... })

    assertAll(...) para agrupar varias aserciones y que se ejecuten todas aunque alguna falle.

Desde JUnit 5.8 se pueden usar aserciones con mensaje como Supplier (() -> "mensaje costoso") para evaluación perezosa.
4. Test parametrizados

Ejecutan un mismo test con múltiples conjuntos de datos.
```java
@ParameterizedTest
@ValueSource(ints = {1, 2, 3, 4, 5})
void testCuadrado(int numero) {
    assertEquals(numero * numero, calc.cuadrado(numero));
}

@ParameterizedTest
@CsvSource({
    "1, 2, 3",
    "0, 0, 0",
    "-1, -1, -2"
})
void testSuma(int a, int b, int resultado) {
    assertEquals(resultado, calc.sumar(a, b));
}
```

Otras fuentes: @MethodSource, @EnumSource, @CsvFileSource, @ArgumentsSource.
5. Ciclo de vida y extensión

El modelo de extensión permite hooks avanzados mediante @ExtendWith.

    SpringExtension para integrar Spring TestContext Framework.

    MockitoExtension para inicializar mocks de Mockito.

    Extensiones propias implementando BeforeEachCallback, AfterEachCallback, etc.

### 6. Testing de hilos virtuales y concurrencia

Con JUnit 5 podemos probar código asíncrono con assertTimeoutPreemptively o utilizando Thread.startVirtualThread dentro de los tests. Para probar concurrencia estructurada, se puede ejecutar un try (scope) { ... } y verificar resultados con assertAll.
7. Tests de integración con testcontainers

Aunque no es parte de JUnit 5, se integra perfectamente. Testcontainers permite arrancar una base de datos real en un contenedor Docker dentro del test, ideal para pruebas de repositorio. La anotación @Testcontainers y el GenericContainer se combinan con JUnit Jupiter.
8. Prácticas recomendadas

    Nombre descriptivo de tests: usar @DisplayName o el método en estilo shouldReturnSum_whenGivenTwoNumbers.

    Seguir la estructura AAA: Arrange, Act, Assert.

    No realizar I/O real en tests unitarios; usar mocks o stubs.

    Limpiar recursos compartidos en @AfterEach.

    Aislar tests: no deben depender del orden de ejecución.

    Ejecutar tests frecuentemente, integrados con Maven/Gradle.

