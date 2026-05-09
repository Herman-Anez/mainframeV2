# Consultas Nativas y Procedimientos Almacenados

Aunque JPQL cubre la mayoría de los casos de uso, a veces es necesario recurrir al SQL nativo para aprovechar toda la potencia del motor de base de datos específico.

---

## 1. ¿Cuándo usar Consultas Nativas?

El SQL nativo es la opción adecuada en los siguientes escenarios:
- Utilizar características específicas del motor (funciones de ventana, operadores espaciales, `FOR UPDATE`, hints del optimizador).
- Invocar procedimientos almacenados complejos.
- Realizar operaciones masivas de actualización con condiciones que JPQL no soporta.
- Consultas con joins extremadamente complejos donde JPQL pierde legibilidad o rendimiento.

---

## 2. @Query con Native Query

Spring Data JPA permite ejecutar SQL nativo simplemente activando el flag `nativeQuery = true` en la anotación `@Query`.

```java
public interface ProductoRepository extends JpaRepository<Producto, Long> {
    @Query(value = "SELECT * FROM productos WHERE nombre ILIKE CONCAT('%', :nombre, '%')", 
           nativeQuery = true)
    List<Producto> buscarPorNombreSimilar(@Param("nombre") String nombre);
}
```

> [!NOTE]
> El resultado se mapea automáticamente a la entidad (o a una proyección) si los nombres de las columnas devueltas coinciden con los atributos de la clase Java.

---

## 3. Proyecciones en Consultas Nativas

Puedes usar interfaces de proyección para capturar resultados de funciones de agregación o consultas parciales:

```java
public interface ProductoCantidad {
    String getCategoria();
    Long getCantidad();
}

@Query(value = "SELECT categoria, COUNT(*) as cantidad FROM productos GROUP BY categoria", 
       nativeQuery = true)
List<ProductoCantidad> contarPorCategoria();
```

> [!TIP]
> Si el SQL devuelve nombres de columna diferentes, utiliza alias en el SQL (`SELECT cat AS categoria`) para que coincidan con los métodos `get` de tu interfaz.

---

## 4. Mapeo a DTOs complejos

Para casos donde necesitas un DTO (clase concreta) y no una interfaz, se utiliza `@SqlResultSetMapping`:

```java
@SqlResultSetMapping(
    name = "productoResumenMapping",
    classes = @ConstructorResult(
        targetClass = ProductoResumenDTO.class,
        columns = {
            @ColumnResult(name = "nombre", type = String.class),
            @ColumnResult(name = "precio_medio", type = Double.class)
        }
    )
)
@Entity
public class Producto { ... }
```

---

## 5. Ejecución Dinámica con EntityManager

Cuando la consulta se construye dinámicamente en tiempo de ejecución, puedes usar el `EntityManager` directamente:

```java
@Repository
public class ProductoCustomRepository {
    @PersistenceContext
    private EntityManager em;

    public List<Producto> buscarConFiltros(Map<String, Object> filtros) {
        StringBuilder sql = new StringBuilder("SELECT * FROM productos WHERE 1=1");
        // ... construcción dinámica del string SQL ...
        Query query = em.createNativeQuery(sql.toString(), Producto.class);
        return query.getResultList();
    }
}
```

> [!CAUTION]
> Ten mucho cuidado con la concatenación de strings para evitar ataques de **SQL Injection**. Usa siempre parámetros enlazados (`setParameter`).

---

## 6. Procedimientos Almacenados

Spring Data JPA facilita la llamada a procedimientos mediante la anotación `@Procedure`:

```java
@Procedure("nombre_procedimiento")
void ejecutarProcedimiento(@Param("param1") String param1);
```

### Alternativa vía EntityManager
Si necesitas un control más fino sobre los parámetros de entrada y salida:

```java
StoredProcedureQuery sp = em.createStoredProcedureQuery("calcular_ventas");
sp.registerStoredProcedureParameter("anio", Integer.class, ParameterMode.IN);
sp.setParameter("anio", 2025);
sp.execute();
List<Object[]> resultados = sp.getResultList();
```

---

## 7. Consideraciones de Seguridad y Portabilidad

> [!IMPORTANT]
> - **Portabilidad**: Las consultas nativas atan tu código a un motor de base de datos específico (ej. Dialecto PostgreSQL vs MySQL).
> - **Caché**: Estas consultas **no pasan por la Caché de Segundo Nivel** de Hibernate.
> - **Validación**: Los errores sintácticos en SQL nativo solo se detectan en tiempo de ejecución, a diferencia de JPQL que suele validarse al arrancar la aplicación.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Spring Data JPA](./Spring_Data_JPA.md) | [Índice](../../index.md) | [Transacciones y @Transactional](./Transacciones_y_Transactional.md) |

