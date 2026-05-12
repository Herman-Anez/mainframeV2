# JMeter Básico (Profundización para SDET)

Apache JMeter es una herramienta de escritorio basada en Java que actúa como cliente de carga. Aunque su interfaz gráfica es útil para el diseño, el SDET la utiliza principalmente en modo no gráfico y la integra en pipelines.

## Arquitectura de un Plan de Pruebas

- **Thread Group (Grupo de Hilos)**: Simula usuarios virtuales. Configuramos:
    - **Número de hilos**: Usuarios concurrentes.
    - **Ramp-up period**: Tiempo que tarda en arrancar todos los hilos.
    - **Loop count**: Iteraciones. Con "Forever" y duración controlada externamente obtenemos pruebas de resistencia.
- **Samplers**: Peticiones concretas (HTTP Request, JDBC Request, etc.). Para APIs REST se usa HTTP Request, configurando método, host, puerto, path, parámetros y cabeceras.
- **Config Elements**: HTTP Header Manager, CSV Data Set Config (para data-driven de carga), HTTP Cookie Manager, etc. Se aplican al nivel adecuado (plan, thread group, sampler).
- **Assertions**: Validan las respuestas. `Response Assertion` para verificar código de estado, presencia de texto, o mediante `JSON Assertion` extraer y comparar campos. Si la aserción falla, la petición se marca como error.
- **Listeners**: Recogen resultados. *View Results Tree*, *Summary Report*, *Aggregate Report*. 
- **Timers**: *Constant Timer*, *Uniform Random Timer* simulan pausas entre peticiones para imitar el comportamiento real del usuario.
- **Logic Controllers**: *If Controller*, *Loop Controller*, *Transaction Controller* (agrupa samplers y mide tiempos de transacción completa).

> [!IMPORTANT]
> En modo línea de comandos, se usan **Simple Data Writer** o backends como **Graphite**. El SDET configura **Backend Listener** para InfluxDB/Grafana y generar informes en tiempo real.

## Diseño de Pruebas

- **Prueba de Carga (Load)**: Carga esperada con rampa suave, se observan tiempos de respuesta y tasas de error.
- **Prueba de Estrés (Stress)**: Aumento progresivo hasta sobrepasar la capacidad para ver cómo se degrada.
- **Prueba de Resistencia (Soak)**: Carga constante durante horas para detectar fugas de memoria.
- **Prueba de Pico (Spike)**: Subida brusca y bajada.

## Automatización con Línea de Comandos y Jenkins

```bash
jmeter -n -t plan.jmx -l resultados.csv -e -o ./reporte/
```

- `-n`: Modo no gráfico.
- `-t`: Archivo de plan.
- `-l`: Archivo de resultados (CSV).
- `-e -o`: Genera dashboard HTML con estadísticas y gráficos.

> [!TIP]
> El SDET parametriza el plan usando propiedades (`-Jhilos=10`) que se leen con `${__P(hilos)}` dentro del `.jmx`.

En Jenkins, un stage de rendimiento ejecuta JMeter, archiva el dashboard y puede usar el plugin **Performance Plugin** para comparar históricos y decidir si el build falla según umbrales (ej. tiempo medio de respuesta < 500ms, % error < 2%).

## Buenas Prácticas

- No incluir listeners pesados en el plan final.
- Usar **CSV Data Set Config** para leer datos de test y simular múltiples usuarios únicos.
- Ejecutar JMeter en modo distribuido para generar más carga, aunque **k6** suele escalar mejor.
- Aislar los inyectores de carga en contenedores o VMs dedicadas para no afectar métricas.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Módulo 05 Index](../index.md) | [Home](../../../index.md) | [k6 Scripts](./k6-scripts.md) |