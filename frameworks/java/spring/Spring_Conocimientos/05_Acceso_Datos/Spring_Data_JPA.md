
# Spring Data JPA

Spring Data JPA simplifica drásticamente el acceso a datos al generar automáticamente las implementaciones de las interfaces de repositorio en tiempo de ejecución. Solo necesitas definir la interfaz y, mediante derivación de consultas o consultas anotadas, obtienes toda la funcionalidad necesaria.

---

## 1. El Paradigma de Repositorios

Al extender de `JpaRepository`, Spring crea automáticamente un proxy que implementa los métodos CRUD básicos, paginación, ordenación y operaciones en lote.

```java
public interface ProductoRepository extends JpaRepository<Producto, Long> {
    List<Producto> findByNombreIgnoreCase(String nombre);
    Optional<Producto> findByNombreAndFabricante(String nombre, Fabricante f);
}
```

> [!TIP]
> `JpaRepository` hereda de `PagingAndSortingRepository` y `CrudRepository`, proporcionando una API muy rica para gestionar el ciclo de vida de tus entidades.

---

## 2. Query Methods: Consultas Derivadas

El mecanismo más potente de Spring Data es la traducción automática del nombre del método a una consulta JPQL.

### Palabras Clave Comunes
| Palabra Clave | Ejemplo | JPQL Equivalente |
| :--- | :--- | :--- |
| `find...By`, `read...By` | `findByNombre` | `WHERE x.nombre = ?1` |
| `Containing`, `Contains` | `findByNombreContaining` | `WHERE x.nombre LIKE %?1%` |
| `StartingWith` | `findByNombreStartingWith` | `LIKE ?1%` |
| `Between` | `findByPrecioBetween` | `WHERE x.precio BETWEEN ?1 AND ?2` |
| `In` | `findByCategoriaIn` | `WHERE x.categoria IN ?1` |
| `OrderBy` | `findByNombreOrderByPrecioDesc` | `ORDER BY x.precio DESC` |
| `True`, `False` | `findByActivoTrue` | `WHERE x.activo = true` |
| `First`, `Top` | `findFirst5ByNombre` | Limita los resultados a los primeros 5 |

> [!NOTE]
> Puedes usar `Pageable` y `Sort` como parámetros adicionales en cualquier consulta derivada para gestionar resultados paginados u ordenados dinámicamente.

---

## 3. Consultas Personalizadas con @Query

Para consultas complejas que no pueden expresarse mediante nombres de métodos o cuando necesitas optimizaciones como `FETCH JOIN`:

```java
@Query("SELECT p FROM Producto p JOIN FETCH p.fabricante WHERE p.nombre LIKE %:nombre%")
List<Producto> buscarPorNombreConFabricante(@Param("nombre") String nombre);
```

### Operaciones de Modificación
Para realizar `UPDATE` o `DELETE` masivos:

```java
@Modifying
@Transactional
@Query("UPDATE Producto p SET p.precio = p.precio * :factor WHERE p.categoria = :cat")
int actualizarPrecioPorCategoria(@Param("factor") BigDecimal factor, @Param("cat") Categoria cat);
```

> [!IMPORTANT]
> La anotación `@Modifying` indica que la consulta no es un `SELECT` y requiere ser ejecutada dentro de una transacción activa (vía `@Transactional`).

---

## 4. @EntityGraph: Control de Carga EAGER/LAZY

Para resolver el problema de las **N+1 consultas** sin escribir JPQL manualmente, puedes usar `@EntityGraph`:

```java
// Definición ad-hoc en el repositorio
@EntityGraph(attributePaths = {"fabricante"})
List<Producto> findAll();
```

---

## 5. Auditoría Automática

Spring Data JPA puede gestionar automáticamente campos de auditoría (quién y cuándo creó/modificó un registro).

```java
@EntityListeners(AuditingEntityListener.class)
@Entity
public class Producto {
    @CreatedDate
    private Instant fechaCreacion;

    @LastModifiedDate
    private Instant fechaModificacion;
}
```

> [!NOTE]
> Para activar esta funcionalidad, debes añadir `@EnableJpaAuditing` en una de tus clases de configuración.

---

## 6. Proyecciones y DTOs

No siempre es eficiente devolver la entidad completa. Las proyecciones basadas en interfaces permiten seleccionar solo las columnas necesarias:

```java
public interface ProductoResumen {
    String getNombre();
    BigDecimal getPrecio();
}

// En el repositorio:
List<ProductoResumen> findByCategoria(Categoria cat);
```

---

## 7. Consultas Dinámicas: Specifications

Cuando necesitas construir filtros de búsqueda dinámicos basados en múltiples criterios, se utiliza `JpaSpecificationExecutor`:

```java
Specification<Producto> spec = (root, query, cb) -> cb.and(
    cb.like(root.get("nombre"), "%" + nombre + "%"),
    cb.greaterThan(root.get("precio"), 10)
);

List<Producto> productos = repo.findAll(spec);
```

---

## 8. Paginación y Streaming

- **`Page<T>`**: Retorna una lista junto con metadatos (total de registros, páginas totales). Ejecuta una consulta `count` adicional.
- **`Slice<T>`**: Indica solo si hay una página siguiente disponible. Más eficiente que `Page` al evitar el `count`.
- **`Stream<T>`**: Permite procesar grandes volúmenes de datos usando Java 8 Streams de forma eficiente. Debe ejecutarse dentro de una transacción.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [JPA y Hibernate Integración](./JPA_y_Hibernate_Integracion.md) | [Índice](../../index.md) | [Consultas Nativas y Procedure](./Consultas_Nativas_y_Procedure.md) |


