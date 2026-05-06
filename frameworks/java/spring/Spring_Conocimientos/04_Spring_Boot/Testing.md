# Spring_Boot/Testing.md
Enfoque de testing en Spring Boot

Spring Boot facilita tanto pruebas unitarias (aisladas, sin contexto) como pruebas de integración (con contexto de Spring y/o bases de datos reales). Su starter spring-boot-starter-test trae: JUnit Jupiter, Mockito, AssertJ, Hamcrest, Spring Test, y más.
Pruebas unitarias con Mockito

No se levanta el contexto Spring; se mockean dependencias.
java

@ExtendWith(MockitoExtension.class)
class ProductoServiceTest {
    @Mock
    ProductoRepository repo;
    @InjectMocks
    ProductoService service;

    @Test
    void buscarPorId_debeRetornarProducto() {
        Producto esperado = new Producto(1L, "Teclado");
        when(repo.findById(1L)).thenReturn(Optional.of(esperado));

        Producto resultado = service.buscarPorId(1L);
        assertThat(resultado.getNombre()).isEqualTo("Teclado");
    }
}

Pruebas de integración con @SpringBootTest

@SpringBootTest levanta el contexto completo (o parcial). Por defecto, busca la clase @SpringBootApplication hacia arriba en el paquete. Útil para pruebas end-to-end de capas completas. Se puede arrancar un servidor real en un puerto aleatorio con webEnvironment = DEFINED_PORT / RANDOM_PORT.
java

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class MiApiIntegrationTest {
    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    void obtenerProductos() {
        ResponseEntity<String> response = restTemplate.getForEntity("/api/productos", String.class);
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
    }
}

Slices de contexto (testing ligero de capas)

Para no levantar todo el contexto y acelerar las pruebas, Boot ofrece anotaciones de "slice":
Anotación	Carga solo	Típico use case
@WebMvcTest	Capa web (controladores), sin servicios ni repos. Mock de dependencias con @MockBean.	Probar controladores REST.
@DataJpaTest	Entidades, repositorios, DataSource embebido. Transaccional y rollback por defecto.	Probar repositorios y queries.
@JsonTest	Solo Jackson (serialización).	Probar DTOs JSON.
@RestClientTest	RestTemplate y componentes de llamada REST.	Probar clientes REST.
@JdbcTest	Solo JDBC (sin JPA).	Probar consultas directas.

Ejemplo @WebMvcTest:
java

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

Nota: @WebMvcTest desactiva la autoconfiguración completa de datos y seguridad, aunque puedes incluir filtros concretos.
Mocking y sobrescritura de beans en tests

    @MockBean: reemplaza un bean en el contexto por un mock de Mockito. Útil para simular dependencias externas.

    @SpyBean: envuelve el bean real con un spy, permitiendo verificar llamadas.

    @TestConfiguration + @Bean: define beans adicionales o sustituye beans para ese test específico (dentro de la clase de test o en una inner class).

    @SpringBootTest(classes = ...) o @Import para cargar solo configuraciones específicas.

Base de datos en pruebas

@DataJpaTest configura automáticamente una base de datos embebida en memoria (H2). Las transacciones se revierten al final de cada test. Puedes usar el parámetro @AutoConfigureTestDatabase(replace = Replace.NONE) para conectar a una base de datos real (p.ej. PostgreSQL en un contenedor).

Para pruebas de integración con una base de datos real, el enfoque moderno es Testcontainers: levanta una instancia Docker de PostgreSQL, MySQL, etc., y la inyecta mediante configuraciones dinámicas (@DynamicPropertySource) o usando el módulo Spring Boot de Testcontainers.
Pruebas con @SpringBootTest y control transaccional

Por defecto, @SpringBootTest no es transaccional (a diferencia de @DataJpaTest). Para pruebas que usan HTTP (TestRestTemplate), ejecutan en hilos separados, por lo que la transacción no se comparte. En esos casos hay que limpiar manualmente o usar @Transactional (solo si las peticiones no cruzan hilos).
Pruebas con configuración externa

Puedes usar @ActiveProfiles("test") y un archivo application-test.properties para definir propiedades específicas. También @TestPropertySource para añadir propiedades en línea.
