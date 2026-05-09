# Testing en Spring Boot

Spring Boot proporciona un ecosistema robusto para el testing, facilitando tanto las pruebas unitarias (aisladas de la infraestructura) como las pruebas de integración (que validan la colaboración entre componentes y el contexto de Spring).

---

## El Starter de Testing

El `spring-boot-starter-test` es la dependencia central que agrupa las mejores librerías del ecosistema:
- **JUnit 5**: El motor estándar de ejecución de pruebas.
- **Mockito**: Para la creación y gestión de dobles de prueba (mocks).
- **AssertJ**: Para aserciones fluidas y legibles.
- **Hamcrest**: Librería de matchers.
- **Spring Test**: Soporte específico para el contexto de Spring.

---

## Pruebas Unitarias con Mockito

En este enfoque no se levanta el contexto de Spring, lo que resulta en una ejecución extremadamente rápida. Se utilizan anotaciones de Mockito para gestionar las dependencias.

```java
@ExtendWith(MockitoExtension.class)
class ProductoServiceTest {
    @Mock
    private ProductoRepository repo;

    @InjectMocks
    private ProductoService service;

    @Test
    void buscarPorId_debeRetornarProducto() {
        Producto esperado = new Producto(1L, "Teclado");
        when(repo.findById(1L)).thenReturn(Optional.of(esperado));

        Producto resultado = service.buscarPorId(1L);

        assertThat(resultado.getNombre()).isEqualTo("Teclado");
        verify(repo).findById(1L);
    }
}
```

---

## Pruebas de Integración con `@SpringBootTest`

`@SpringBootTest` arranca el contexto completo de la aplicación. Es ideal para pruebas end-to-end o cuando se necesita validar la interacción real entre capas.

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class MiApiIntegrationTest {
    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    void obtenerProductos_debeRetornarOk() {
        ResponseEntity<String> response = restTemplate.getForEntity("/api/productos", String.class);
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
    }
}
```

> [!NOTE]
> `webEnvironment = RANDOM_PORT` evita conflictos de puertos al ejecutar pruebas en paralelo o en servidores de CI/CD.

---

## Slices de Contexto (Testing Ligero)

Para acelerar las pruebas sin perder la potencia del contexto, Spring Boot ofrece "slices" que cargan solo los componentes necesarios para una capa específica.

| Anotación | Carga Solo... | Caso de Uso Típico |
| :--- | :--- | :--- |
| `@WebMvcTest` | Capa Web (Controladores, Filtros). | Validar rutas REST y serialización JSON. |
| `@DataJpaTest` | Capa de Datos (Entidades, Repositorios). | Validar consultas JPQL/SQL. |
| `@JsonTest` | Serialización/Deserialización Jackson. | Validar el mapeo de DTOs a JSON. |
| `@RestClientTest` | Clientes REST (RestTemplate). | Probar integraciones con APIs externas. |

### Ejemplo: `@WebMvcTest`
Permite probar controladores mockeando los servicios mediante `@MockBean`.

```java
@WebMvcTest(ProductoController.class)
class ProductoControllerTest {
    @Autowired
    private MockMvc mvc;

    @MockBean
    private ProductoService service;

    @Test
    void listarDebeRetornarOk() throws Exception {
        when(service.listar()).thenReturn(List.of(new Producto()));

        mvc.perform(get("/api/productos"))
           .andExpect(status().isOk())
           .andExpect(content().contentType(MediaType.APPLICATION_JSON));
    }
}
```

---

## Gestión de Datos y Bases de Datos

### Bases de Datos en Memoria
`@DataJpaTest` configura automáticamente una base de datos embebida (como H2). Por defecto, todas las pruebas son **transaccionales** y realizan rollback al finalizar, manteniendo la BD limpia para el siguiente test.

### Testcontainers
Para pruebas de integración contra bases de datos reales (PostgreSQL, MySQL), el estándar actual es **Testcontainers**, que levanta contenedores Docker efímeramente para la ejecución de la suite.

---

## Configuración y Perfiles de Test

Es una buena práctica separar la configuración de pruebas de la de producción.

- **`@ActiveProfiles("test")`**: Activa el archivo `application-test.yml`.
- **`@TestPropertySource`**: Permite inyectar o sobrescribir propiedades específicas solo para una clase de test.
- **`@TestConfiguration`**: Permite definir beans adicionales o sustituir beans existentes dentro de un test.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Actuator y Métricas](./Actuator_y_Metricas.md) | [Índice](../../index.md) | [JDBC Template](../05_Acceso_Datos/JDBC_Template.md) |

