# Acceso_Datos/Consultas_Nativas_y_Procedure.md
Cuándo usar consultas nativas

Aunque JPQL cubre la mayoría de casos, a veces es necesario SQL nativo para:

    Utilizar características específicas del motor (funciones de ventana, operadores espaciales, FOR UPDATE, hints de optimizador).

    Invocar procedimientos almacenados complejos.

    Realizar operaciones masivas de actualización con condiciones especiales.

    Consultas con joins complejos donde JPQL no rinde o se vuelve ilegible.

Spring Data JPA y JPA proveen mecanismos para ejecutar SQL nativo manteniendo el mapeo de resultados.
@Query con nativeQuery = true
java

public interface ProductoRepository extends JpaRepository<Producto, Long> {
    @Query(value = "SELECT * FROM productos WHERE nombre ILIKE CONCAT('%', :nombre, '%')", 
           nativeQuery = true)
    List<Producto> buscarPorNombreSimilar(@Param("nombre") String nombre);
}

El resultado se mapea a la entidad Producto (o una proyección) si las columnas coinciden. También se puede retornar Object[] o List<Object[]> para casos sin mapeo.
Proyecciones con consulta nativa

Con una interfaz de proyección:
java

public interface ProductoCantidad {
    String getCategoria();
    Long getCantidad();
}

@Query(value = "SELECT categoria, COUNT(*) as cantidad FROM productos GROUP BY categoria", nativeQuery = true)
List<ProductoCantidad> contarPorCategoria();

Si el SQL devuelve columnas con nombres diferentes, se puede usar alias (SELECT cat as categoria).
Mapeo a DTO con @SqlResultSetMapping

Cuando se necesita un DTO (clase concreta) en lugar de interfaz, se puede usar @SqlResultSetMapping:
java

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

// Luego en el repositorio:
@Query(value = "SELECT nombre, AVG(precio) as precio_medio FROM productos GROUP BY nombre", nativeQuery = true)
@SqlResultSetMapping(name = "productoResumenMapping")  // redundante si ya se mapea en la entidad
List<ProductoResumenDTO> resumenPrecios();

En la práctica, se prefiere @NamedNativeQuery declarado en la entidad y luego invocarlo con EntityManager.createNamedQuery.
Ejecución dinámica de SQL nativo con EntityManager

Cuando la consulta se construye en tiempo de ejecución (cuidado con SQL injection), se puede usar EntityManager.createNativeQuery directamente en el repositorio o un DAO.
java

@Repository
public class ProductoCustomRepository {
    @PersistenceContext
    private EntityManager em;

    @SuppressWarnings("unchecked")
    public List<Producto> buscarConFiltros(Map<String, Object> filtros) {
        StringBuilder sql = new StringBuilder("SELECT * FROM productos WHERE 1=1");
        Map<String, Object> params = new HashMap<>();
        if (filtros.containsKey("nombre")) {
            sql.append(" AND nombre LIKE :nombre");
            params.put("nombre", "%" + filtros.get("nombre") + "%");
        }
        Query query = em.createNativeQuery(sql.toString(), Producto.class);
        params.forEach(query::setParameter);
        return query.getResultList();
    }
}

Llamada a procedimientos almacenados con @Procedure

Spring Data JPA permite invocar procedimientos almacenados mediante la anotación @Procedure en métodos del repositorio.
java

@Procedure("nombre_procedimiento")
void ejecutarProcedimiento(@Param("param1") String param1);

Si el procedimiento retorna un conjunto de resultados, se puede declarar el tipo de retorno List<T>. También se puede usar @Query con nativeQuery = true y CALL para procedimientos que no se adaptan a los parámetros.

Alternativa vía EntityManager:
java

StoredProcedureQuery sp = em.createStoredProcedureQuery("calcular_ventas");
sp.registerStoredProcedureParameter("anio", Integer.class, ParameterMode.IN);
sp.setParameter("anio", 2025);
sp.execute();
List<Object[]> resultados = sp.getResultList();

Actualizaciones masivas con SQL nativo

@Modifying también funciona con nativeQuery = true:
java

@Modifying
@Transactional
@Query(value = "UPDATE productos SET precio = precio * 1.1 WHERE categoria = :cat", nativeQuery = true)
int aplicarInflacion(@Param("cat") String categoria);

Ojo: al ser nativo, no se aplican las reglas de cascada JPA ni se actualizan entidades en memoria, por lo que debe ir seguido de una recarga si la sesión se mantiene.
Consideraciones de seguridad y portabilidad

    Las consultas nativas atan la aplicación a un dialecto de base de datos concreto.

    Mayor riesgo de SQL injection si se concatenan parámetros. Siempre usar parámetros enlazados (setParameter).

    No pasan por la caché de segundo nivel de Hibernate.

    Las consultas nativas no son validadas en tiempo de arranque (salvo que se habilite spring.jpa.properties.hibernate.query.fail_on_pagination_over_collection_fetch), así que los errores sintácticos aparecen en tiempo de ejecución.



//////////////////////////////////////////////////////////////
