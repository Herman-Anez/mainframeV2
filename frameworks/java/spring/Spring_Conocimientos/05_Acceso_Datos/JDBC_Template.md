# JDBC Template en Spring

JDBC es potente pero requiere mucho código repetitivo: abrir conexiones, preparar sentencias, recorrer `ResultSet`, cerrar recursos en bloques `finally` anidados y manejar la omnipresente `SQLException`. Spring elimina esa fricción con **JdbcTemplate**, que sigue el patrón *Template Method*: el recurso se abre y cierra automáticamente, y tu código se centra únicamente en la lógica SQL y el mapeo.

---

## 1. Configuración del DataSource

Todo comienza con un `DataSource`. Spring Boot lo autoconfigura a partir de las propiedades `spring.datasource.*`. Si no hay propiedades, intenta usar una base de datos embebida (como H2) si encuentra el driver en el classpath.

### Configuración manual
Si necesitas definirlo manualmente:

```java
@Bean
public DataSource dataSource() {
    HikariConfig config = new HikariConfig();
    config.setJdbcUrl("jdbc:mysql://localhost/midb");
    config.setUsername("user");
    config.setPassword("pass");
    return new HikariDataSource(config);
}

@Bean
public JdbcTemplate jdbcTemplate(DataSource ds) {
    return new JdbcTemplate(ds);
}
```

> [!TIP]
> Spring Boot incluye **HikariCP** como pool de conexiones por defecto, ya que es actualmente el más rápido y eficiente para la JVM.

---

## 2. Operaciones básicas con JdbcTemplate

Una vez inyectado `JdbcTemplate`, los métodos principales para interactuar con la base de datos son:

- **`queryForObject(String sql, Class<T> tipo, Object... args)`**: Para obtener un solo valor (ej. `count`). Lanza `EmptyResultDataAccessException` si no hay resultados.
- **`queryForList(String sql, Class<T> tipo, Object... args)`**: Retorna una lista de valores únicos.
- **`query(String sql, RowMapper<T> rowMapper, Object... args)`**: Retorna una lista de objetos mapeados.
- **`queryForMap(String sql, Object... args)`**: Retorna un solo registro como un `Map<String, Object>`.
- **`update(String sql, Object... args)`**: Para operaciones `INSERT`, `UPDATE` y `DELETE`. Devuelve el número de filas afectadas.
- **`batchUpdate(String sql, List<Object[]> batchArgs)`**: Ejecuta múltiples actualizaciones en lote.
- **`execute(String sql)`**: Para sentencias DDL o ejecución genérica.

---

## 3. RowMapper: El puente entre ResultSet y Objetos

La interfaz funcional `RowMapper` es clave para transformar las filas de la base de datos en objetos Java.

```java
public class ProductoRowMapper implements RowMapper<Producto> {
    @Override
    public Producto mapRow(ResultSet rs, int rowNum) throws SQLException {
        Producto p = new Producto();
        p.setId(rs.getLong("id"));
        p.setNombre(rs.getString("nombre"));
        p.setPrecio(rs.getBigDecimal("precio"));
        return p;
    }
}
```

### Alternativas de mapeo
- **Lambdas**: Se puede simplificar como `(rs, rowNum) -> new Producto(...)`.
- **BeanPropertyRowMapper**: Spring proporciona `BeanPropertyRowMapper<Producto>(Producto.class)` que mapea automáticamente por nombres de columna (si coinciden con los atributos), aunque es ligeramente más lento y menos flexible que un mapeo manual.

---

## 4. NamedParameterJdbcTemplate

En lugar de usar el signo de interrogación `?`, puedes usar parámetros con nombre (ej. `:id`). Esto requiere un `NamedParameterJdbcTemplate`.

```java
String sql = "SELECT * FROM productos WHERE nombre = :nombre AND precio < :precio";
Map<String, Object> params = Map.of("nombre", "Teclado", "precio", new BigDecimal(100));
List<Producto> productos = namedJdbcTemplate.query(sql, params, new ProductoRowMapper());
```

> [!NOTE]
> Usar parámetros con nombre es muy práctico cuando las consultas tienen muchos parámetros, ya que mejora significativamente la legibilidad y reduce errores de orden.

---

## 5. ResultSetExtractor y RowCallbackHandler

- **ResultSetExtractor**: Útil para procesar el `ResultSet` completo dentro de una sola callback. Por ejemplo, para construir una estructura jerárquica (como un objeto con una lista anidada) a partir de múltiples filas.
- **RowCallbackHandler**: Procesa fila a fila sin devolver nada. Es ideal para tareas de volcado de datos o streaming de grandes volúmenes donde no queremos acumular todo en memoria.

---

## 6. Gestión de Excepciones

JDBC estándar lanza `SQLException` (checked). `JdbcTemplate` traduce automáticamente estas excepciones a la jerarquía de **`DataAccessException`** de Spring.

> [!IMPORTANT]
> Las `DataAccessException` son **unchecked** (runtime) y mucho más informativas: `DataIntegrityViolationException`, `DuplicateKeyException`, `BadSqlGrammarException`, etc. Esto desacopla tu lógica de negocio de las peculiaridades del driver JDBC.

---

## 7. Operaciones por lotes (Batch)

Para insertar miles de registros de forma eficiente:

```java
List<Object[]> batch = productos.stream()
    .map(p -> new Object[]{p.getNombre(), p.getPrecio()})
    .collect(toList());

jdbcTemplate.batchUpdate("INSERT INTO productos (nombre, precio) VALUES (?,?)", batch);
```

### Recuperación de claves generadas
Si necesitas el ID generado tras un insert:

```java
KeyHolder keyHolder = new GeneratedKeyHolder();
jdbcTemplate.update(connection -> {
    PreparedStatement ps = connection.prepareStatement(
        "INSERT INTO productos (nombre, precio) VALUES (?,?)", 
        Statement.RETURN_GENERATED_KEYS);
    ps.setString(1, p.getNombre());
    ps.setBigDecimal(2, p.getPrecio());
    return ps;
}, keyHolder);

Long nuevoId = keyHolder.getKey().longValue();
```

---

## 8. Llamada a Procedimientos Almacenados

Aunque se puede usar `JdbcTemplate.call(...)`, Spring ofrece **`SimpleJdbcCall`** para simplificar la interacción:

```java
SimpleJdbcCall jdbcCall = new SimpleJdbcCall(jdbcTemplate)
    .withProcedureName("actualizar_stock")
    .declareParameters(
        new SqlParameter("p_id", Types.INTEGER),
        new SqlParameter("p_cantidad", Types.INTEGER));

Map<String, Object> inParams = Map.of("p_id", id, "p_cantidad", cantidad);
jdbcCall.execute(inParams);
```

---

## 9. ¿Cuándo usar JdbcTemplate frente a JPA?

Deberías considerar `JdbcTemplate` en los siguientes escenarios:
1. Cuando necesitas **control absoluto** sobre el SQL ejecutado.
2. Para obtener el **rendimiento máximo** en consultas complejas.
3. En aplicaciones pequeñas donde un ORM completo como Hibernate sería excesivo.
4. Cuando el modelo de datos no se mapea limpiamente a entidades (ej. reportes complejos).
5. Para tareas de **migración de datos** o procesos batch masivos.

> [!NOTE]
> Spring también ofrece **Spring Data JDBC**, que combina el estilo de repositorios de Spring Data con la simplicidad de JDBC, sin la complejidad del estado gestionado de JPA.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | :--- |
| [← Testing en Spring Boot](../04_Spring_Boot/Testing.md) | [Índice](../../README.md) | [Integración de JPA y Hibernate →](JPA_y_Hibernate_Integracion.md) |

