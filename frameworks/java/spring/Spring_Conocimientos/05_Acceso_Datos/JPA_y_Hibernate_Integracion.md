# Acceso_Datos/JPA_y_Hibernate_Integracion.md
JPA: estándar, Hibernate: implementación

JPA (Jakarta Persistence API) es la especificación estándar para ORM en Java. Hibernate es la implementación más popular. Spring Boot elige Hibernate automáticamente si está en el classpath (starter spring-boot-starter-data-jpa).
Configuración sin Spring Boot

En Spring puro, configurar JPA implica:
java

@Bean
public LocalContainerEntityManagerFactoryBean entityManagerFactory(DataSource ds) {
    LocalContainerEntityManagerFactoryBean emf = new LocalContainerEntityManagerFactoryBean();
    emf.setDataSource(ds);
    emf.setPackagesToScan("com.empresa.modelo");
    emf.setJpaVendorAdapter(new HibernateJpaVendorAdapter());
    emf.setJpaProperties(hibernateProperties());
    return emf;
}

@Bean
public PlatformTransactionManager transactionManager(EntityManagerFactory emf) {
    return new JpaTransactionManager(emf);
}

Spring Boot autoconfigura todo esto con un simple spring.jpa.* en las propiedades.
El EntityManager y su ciclo de vida

El EntityManager es el objeto central de JPA que gestiona las entidades. Spring, a través de la anotación @PersistenceContext, inyecta un EntityManager con ámbito de transacción. En realidad inyecta un proxy que comparte el EntityManager real (que es de ámbito de transacción y no es thread-safe).
java

@Repository
public class ProductoDao {
    @PersistenceContext
    private EntityManager em;

    public Producto findById(Long id) {
        return em.find(Producto.class, id);
    }
}

Entidades: anotaciones esenciales
java

@Entity
@Table(name = "productos")
public class Producto {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 200)
    private String nombre;

    @Enumerated(EnumType.STRING)
    private Categoria categoria;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "fabricante_id")
    private Fabricante fabricante;
    // getters/setters
}

Estrategias de generación de ID: AUTO, IDENTITY, SEQUENCE, TABLE. Lo más común es IDENTITY (autoincrement) o SEQUENCE en bases de datos que lo soportan (PostgreSQL, Oracle).
Mapeo de relaciones

    @OneToOne, @OneToMany, @ManyToOne, @ManyToMany.

    Importante: FetchType.LAZY para evitar cargas innecesarias (el valor por defecto en @ManyToOne es EAGER, así que hay que cambiarlo).

    Cuidado con @OneToMany sin mappedBy: por defecto crea tabla intermedia. Generalmente se define mappedBy en el lado no propietario.

    LazyInitializationException: ocurre cuando se accede a una relación lazy fuera de la transacción. Para evitarlo: usar JOIN FETCH en consultas, mantener transacción abierta (con @Transactional sobre el método) o usar DTOs.

Hibernate como motor: propiedades clave
properties

spring.jpa.show-sql=true
spring.jpa.hibernate.ddl-auto=validate  # none, update, create, create-drop
spring.jpa.properties.hibernate.format_sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect
spring.jpa.properties.hibernate.default_schema=public

ddl-auto en producción debe ser validate o none. update puede generar cambios destructivos. Mejor usar Flyway o Liquibase.
Contexto de persistencia y caché de primer nivel

Dentro de una transacción, el EntityManager mantiene un contexto de persistencia (caché de primer nivel) que garantiza que una misma entidad por ID devuelva la misma instancia. Las modificaciones se detectan al hacer flush (antes del commit) mediante el mecanismo de dirty checking, comparando el estado actual con una instantánea del momento de carga. No es necesario llamar a update() explícito; si la entidad está managed y la transacción se completa, Hibernate sincroniza los cambios.
Operaciones con EntityManager

    persist(entity): guarda una nueva entidad.

    merge(entity): actualiza una entidad detached (o crea si no existe).

    remove(entity): elimina una entidad managed.

    find(Class, id): busca por clave primaria.

    createQuery(jpql): consultas JPQL.

    createNativeQuery(sql): consultas nativas.

    flush(): sincroniza con la base de datos sin hacer commit.

Spring Data JPA encapsula todo esto, pero conocer el EntityManager es vital para casos complejos o cuando se requieren consultas dinámicas.
Errores frecuentes

    N+1 queries: al recorrer una colección de entidades que tienen una relación lazy y no se ha hecho fetch, se ejecuta una consulta adicional por cada entidad. Solución: JOIN FETCH en JPQL o @EntityGraph.

    Entidades detachadas: si intentas persistir una entidad que ya tiene ID pero no está managed, puede lanzar PersistentObjectException.

    Transaccionalidad: olvidar @Transactional en el servicio que orquesta múltiples operaciones.
