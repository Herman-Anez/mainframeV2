# Temas_Avanzados/Batch_y_Tareas_Programadas.md
Spring Batch: procesamiento de grandes volúmenes

Spring Batch es un framework para el desarrollo de procesos batch robustos, con reinicio, trazabilidad, control de transacciones escalonado y estadísticas. Una tarea batch se define como un Job compuesto de uno o más Step.

Conceptos básicos:

    Job: una unidad de trabajo completa, compuesto de pasos.

    Step: fase independiente (p.ej. leer, procesar, escribir).

    ItemReader: lee elementos uno a uno de una fuente (BD, archivo plano, XML).

    ItemProcessor: transforma un elemento leído.

    ItemWriter: escribe un lote de elementos (BD, archivo).

    Tasklet: alternativa al chunk para acciones simples (ej. mover archivos, enviar correos).

    JobRepository: almacena metadatos del estado del job y pasos (en BD). Permite reanudar tras fallos.

    JobLauncher: interfaz para lanzar jobs.

Configuración de un Job simple (lectura de CSV a BD)
java

@Configuration
@EnableBatchProcessing
public class BatchConfig {

    @Autowired JobBuilderFactory jobs;
    @Autowired StepBuilderFactory steps;

    @Bean
    public FlatFileItemReader<Producto> reader() {
        return new FlatFileItemReaderBuilder<Producto>()
            .name("productoItemReader")
            .resource(new ClassPathResource("productos.csv"))
            .delimited()
            .names(new String[]{"nombre", "precio"})
            .fieldSetMapper(fieldSet -> {
                Producto p = new Producto();
                p.setNombre(fieldSet.readString("nombre"));
                p.setPrecio(fieldSet.readBigDecimal("precio"));
                return p;
            })
            .linesToSkip(1)
            .build();
    }

    @Bean
    public JdbcBatchItemWriter<Producto> writer(DataSource dataSource) {
        return new JdbcBatchItemWriterBuilder<Producto>()
            .dataSource(dataSource)
            .sql("INSERT INTO productos (nombre, precio) VALUES (:nombre, :precio)")
            .beanMapped()
            .build();
    }

    @Bean
    public Step importStep(FlatFileItemReader<Producto> reader, JdbcBatchItemWriter<Producto> writer) {
        return steps.get("importStep")
            .<Producto, Producto>chunk(10)  // chunk size
            .reader(reader)
            .processor(processor())
            .writer(writer)
            .build();
    }

    @Bean
    public Job importJob(Step importStep, JobCompletionNotificationListener listener) {
        return jobs.get("importJob")
            .incrementer(new RunIdIncrementer())
            .listener(listener)
            .start(importStep)
            .build();
    }

    @Bean
    public ItemProcessor<Producto, Producto> processor() {
        return p -> { 
            p.setNombre(p.getNombre().toUpperCase());
            return p;
        };
    }
}

Chunk-oriented processing

El Step de tipo chunk lee elementos uno a uno con el ItemReader, los acumula en un buffer del tamaño del chunk, los pasa al ItemProcessor (opcional) y luego escribe el chunk completo con el ItemWriter. Si falla, puede reintentar el chunk o marcar el step como fallido.
Tasklets para pasos simples

Cuando no hay necesidad de procesar elementos, se usa un Tasklet:
java

@Bean
public Step cleanupStep() {
    return steps.get("cleanupStep")
        .tasklet((contribution, chunkContext) -> {
            // limpiar archivos temporales
            return RepeatStatus.FINISHED;
        })
        .build();
}

Job scheduling: lanzamiento bajo demanda

Spring Batch no incluye un planificador, pero se integra fácilmente con Spring @Scheduled o herramientas externas como Quartz. En una aplicación Boot, se puede lanzar con JobLauncher desde un controlador o una tarea programada.
java

@RestController
public class BatchController {
    @Autowired JobLauncher jobLauncher;
    @Autowired Job importJob;

    @PostMapping("/batch/import")
    public String lanzar() throws Exception {
        JobExecution exec = jobLauncher.run(importJob, new JobParametersBuilder()
            .addLong("time", System.currentTimeMillis())
            .toJobParameters());
        return "Batch lanzado: " + exec.getStatus();
    }
}

Spring Boot y Batch

El starter spring-boot-starter-batch autoconfigura JobLauncher, JobRepository (necesitarás una base de datos) y habilita @EnableBatchProcessing. Boot puede ejecutar jobs al arrancar si se configura spring.batch.job.enabled=true y se definen beans de Job.
Tareas programadas con @Scheduled

Spring proporciona un planificador ligero para ejecutar métodos periódicamente.

Habilitar con @EnableScheduling en alguna configuración.
java

@Configuration
@EnableScheduling
public class SchedulingConfig { }

Luego en cualquier bean:
java

@Component
public class ReporteProgramado {
    @Scheduled(fixedDelay = 60000) // 60 seg después de que termine la ejecución anterior
    public void generarReporte() { ... }

    @Scheduled(fixedRate = 60000)  // cada 60 seg, independientemente del tiempo de ejecución
    public void refrescarDatos() { ... }

    @Scheduled(cron = "0 0 2 * * ?") // a las 2 AM diario
    public void limpiarLogs() { ... }
}

Opciones:

    fixedDelay: intervalo en ms entre el final de una ejecución y el inicio de la siguiente.

    fixedRate: intervalo entre inicios de ejecución (puede solaparse si la tarea tarda más que el rate; evitar con @Async o manejo de concurrencia).

    initialDelay: retardo antes de la primera ejecución.

    cron: expresión cron (segundos, minutos, horas, día del mes, mes, día de la semana).

    zone: zona horaria para cron.

    timeUnit (a partir de Spring Boot 3.x): permite cambiar la unidad de tiempo.

Ejecución asíncrona de tareas programadas

Por defecto, las tareas @Scheduled se ejecutan en un único hilo (el TaskScheduler). Si una tarea se bloquea, las demás esperan. Para paralelismo, se puede configurar un TaskScheduler con pool:
java

@Bean
public TaskScheduler taskScheduler() {
    ThreadPoolTaskScheduler scheduler = new ThreadPoolTaskScheduler();
    scheduler.setPoolSize(5);
    return scheduler;
}

O marcar la tarea con @Async y habilitar @EnableAsync.
Consideraciones en tareas programadas

    En entornos clusterizados, las tareas programadas en cada nodo se ejecutarán simultáneamente a menos que se use un ejecutor distribuido (como ShedLock, Quartz con JDBC). Para evitar duplicados, se puede usar @SchedulerLock de ShedLock.

    Excepciones no capturadas detienen la ejecución futura de esa tarea con fixedDelay (si la instancia no está ya en ejecución). Es recomendable envolver la lógica en try/catch si se desea que continúe.

    Spring Boot expone el endpoint /actuator/scheduledtasks (Actuator) para ver las tareas programadas y sus expresiones cron.


