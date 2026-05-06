
# Acceso_Datos/Spring_Data_JPA.md
El paradigma: repositorios sin implementación

Spring Data JPA genera automáticamente la implementación de las interfaces de repositorio en tiempo de ejecución. Solo defines la interfaz y, mediante query derivation o consultas anotadas, obtienes el código necesario.
java

public interface ProductoRepository extends JpaRepository<Producto, Long> {
    List<Producto> findByNombreIgnoreCase(String nombre);
    Optional<Producto> findByNombreAndFabricante(String nombre, Fabricante f);
}

En tiempo de arranque, Spring crea un proxy que implementa ProductoRepository y todos los métodos de JpaRepository (CRUD básico, paginación, ordenación, batch).
Query Methods (consulta derivada del nombre)

El mecanismo clave: el nombre del método se analiza y se traduce a una consulta JPQL/Criteria.

Palabras clave más comunes:
Palabra	Ejemplo	JPQL equivalente
find...By, read...By, get...By	findByNombre	where x.nombre = ?1
...Containing / ...Contains	findByNombreContaining(String)	where x.nombre like %?1%
...StartingWith	findByNombreStartingWith	like ?1%
...Between	findByPrecioBetween	where x.precio between ?1 and ?2
...In	findByCategoriaIn	where x.categoria in ?1
...OrderBy	findByNombreOrderByPrecioDesc	order by x.precio desc
...And, ...Or	findByNombreAndPrecio	where x.nombre = ?1 and x.precio = ?2
...True / ...False	findByActivoTrue	where x.activo = true
...First / ...Top	findFirst5ByNombre	limita resultados

Se puede usar Pageable y Sort como parámetro adicional. Retornar Page, List, Stream, opcional con Optional.
java

Page<Producto> findByPrecioGreaterThan(BigDecimal precio, Pageable pageable);

@Query personalizada con JPQL

Cuando los nombres se vuelven muy largos o necesitas joins complejos:
java

@Query("SELECT p FROM Producto p JOIN FETCH p.fabricante WHERE p.nombre LIKE %:nombre%")
List<Producto> buscarPorNombreConFabricante(@Param("nombre") String nombre);

También se pueden hacer updates/delete:
java

@Modifying
@Transactional
@Query("UPDATE Producto p SET p.precio = p.precio * :factor WHERE p.categoria = :cat")
int actualizarPrecioPorCategoria(@Param("factor") BigDecimal factor, @Param("cat") Categoria cat);

@Modifying indica que no es SELECT y necesita @Transactional.
@EntityGraph para controlar carga EAGER/LAZY

Para evitar el problema N+1 sin escribir JPQL, se pueden definir @EntityGraph y referenciarlo en el método:
java

@Entity
@NamedEntityGraph(name = "Producto.fabricante", 
    attributeNodes = @NamedAttributeNode("fabricante"))
public class Producto { ... }

// En repositorio:
@EntityGraph("Producto.fabricante")
List<Producto> findAll();

También se puede definir de forma ad-hoc con @EntityGraph(attributePaths = {"fabricante"}).
Auditoría y campos automáticos

Spring Data JPA proporciona anotaciones para auditoría:

    @CreatedDate, @LastModifiedDate (en java.time.Instant o LocalDateTime).

    @CreatedBy, @LastModifiedBy (con Spring Security integrado).

    Se habilita con @EnableJpaAuditing en alguna configuración.

java

@EntityListeners(AuditingEntityListener.class)
@Entity
public class Producto {
    @CreatedDate
    private Instant fechaCreacion;
    @LastModifiedDate
    private Instant fechaModificacion;
}

Proyecciones y DTOs

En lugar de devolver la entidad completa, se pueden definir interfaces de proyección:
java

public interface ProductoResumen {
    String getNombre();
    BigDecimal getPrecio();
}

// En repositorio:
List<ProductoResumen> findByCategoria(Categoria cat);

Spring solo selecciona las columnas necesarias. También hay proyecciones de cierre abierto (expresiones SpEL) o basadas en DTOs con constructor.
Especificaciones (Specification) y Query by Example

Para consultas dinámicas, JpaSpecificationExecutor permite construir criterios con Specification:
java

public interface ProductoRepository extends JpaRepository<Producto, Long>, 
        JpaSpecificationExecutor<Producto> {}

java

Specification<Producto> spec = (root, query, cb) -> cb.and(
    cb.like(root.get("nombre"), "%" + nombre + "%"),
    cb.greaterThan(root.get("precio"), 10)
);
List<Producto> productos = repo.findAll(spec);

Query by Example permite consultar a partir de una instancia de la entidad con campos no nulos. Simple pero limitado a igualdades exactas.
Paginación, ordenación y streaming

    Page<T>: contiene el contenido, número de página, total páginas, etc.

    Slice<T>: solo sabe si hay siguiente (más eficiente sin count).

    Stream<T>: un stream de resultados que debe cerrarse dentro de una transacción (@Transactional). Bueno para procesar grandes volúmenes con Java 8 streams.

