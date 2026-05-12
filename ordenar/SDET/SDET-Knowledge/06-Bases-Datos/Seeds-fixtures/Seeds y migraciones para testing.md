# Seeds y Migraciones para Testing

El término "seeds" se refiere a datos de referencia que pueblan la base de datos antes de la ejecución de pruebas (catálogos, tipos de cuenta, roles). El SDET los gestiona con herramientas de migración.

## Flyway / Liquibase

- **Migraciones de Datos**: Se pueden aplicar migraciones que inserten datos de prueba en entornos de testing (`V1__insert_categories.sql`).
- **Control de Entorno**: Estas migraciones solo deben ejecutarse en entornos no productivos, mediante perfiles de Spring o configuraciones condicionales.
- **Alternativa**: Usar scripts SQL en la carpeta `test/resources/db/testdata` que se ejecutan antes de cada suite con anotaciones `@Sql` (Spring) o manualmente en el `setUp`.

## Estrategias de Limpieza

1.  **Borrado selectivo**: Al finalizar cada clase de test, se eliminan los datos creados por ID.
2.  **Borrado total y recreación**: Para suites pequeñas, se puede recalcular toda la BD desde cero con Flyway/Liquibase y luego insertar seeds. Es más lento pero garantiza un estado 100% limpio.
3.  **Base de datos por sesión**: Usar Docker para crear una base de datos nueva y destruirla al final. Con **Testcontainers** esto es transparente.

### Ejemplo con Testcontainers (Java)
```java
@Container
static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15")
    .withDatabaseName("test")
    .withUsername("test")
    .withPassword("test");

@BeforeAll
static void init() {
    DataSource ds = DataSourceBuilder.create()
        .url(postgres.getJdbcUrl())
        .username(postgres.getUsername())
        .password(postgres.getPassword())
        .build();
    Flyway.configure().dataSource(ds).load().migrate();
    // Insertar seeds adicionales aquí
}
```

> [!IMPORTANT]
> **Data Factories y Paralelismo**: Cuando las pruebas se ejecutan en paralelo, las fábricas deben manejar la concurrencia. Se recomienda usar `ThreadLocal` para el listado de objetos creados o asegurar valores únicos (UUID) para evitar colisiones.

## Conclusión

Dominar la interacción con bases de datos, ya sean relacionales o NoSQL, y la creación sistemática de datos permite al SDET escribir pruebas robustas, rápidas y altamente fiables.

> [!TIP]
> La clave es tratar los datos como parte del código de prueba, aplicando las mismas buenas prácticas de diseño que en el código de producción.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Data Factories](./Data-factories.md) | [Home](../../index.md) | [Próximo Módulo](../../07-Temas-Avanzados/index.md) |
