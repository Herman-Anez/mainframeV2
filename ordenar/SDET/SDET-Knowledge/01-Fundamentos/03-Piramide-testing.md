# Pirámide de Testing (Profundización)

La pirámide de testing de Mike Cohn (2009) es el modelo mental más importante para un SDET. No es una regla rígida, sino una guía de proporciones y velocidad.

## Capas clásicas y propósito

```text
        /\
       /  \          UI / End-to-End
      /    \         (Pocas, lentas, frágiles)
     /------\
    /        \       Integración / Servicio
   /          \      (Cantidad media, velocidad media)
  /------------\
 /              \    Unitarias
/________________\   (Muchas, rápidas, estables)
```

### 1. Pruebas Unitarias (base)

*   **Qué prueban**: La unidad más pequeña de código aislada (función, método, clase). Sin dependencias externas reales (se usan dobles como mocks/stubs).
*   **Quién las escribe**: Principalmente desarrolladores, pero el SDET define el framework, las políticas de cobertura y las complementa.
*   **Características**: Ejecución en milisegundos, no requieren entorno (todo en memoria). Deben ser miles.
*   **Ejemplo**: Verificar que un método `CalcularDescuento(precio, porcentaje)` devuelve el valor correcto con distintos parámetros.

### 2. Pruebas de Servicio/Integración (capa intermedia)

*   **Qué prueban**: La comunicación entre módulos, APIs, acceso a base de datos, colas de mensajes, contratos entre servicios.
*   **Rol del SDET**: Aquí es donde el SDET más brilla. Automatiza pruebas de API REST, GraphQL, gRPC, mensajería asíncrona (Kafka), pruebas de contrato (Pact) y de integración con bases de datos.
*   **Características**: Más lentas que las unitarias (implican red, E/S). Se ejecutan contra servicios reales, a veces en contenedores Docker. Debe haber muchas, pero en menor cantidad que las unitarias.
*   **Ejemplo**: Enviar una petición POST a `/usuarios` y validar que el código de estado es 201, el cuerpo contiene un ID y que el registro se insertó realmente en la base de datos.

### 3. Pruebas de UI / End-to-End (punta)

*   **Qué prueban**: Flujos completos a través de la interfaz de usuario (web, móvil) simulando un usuario real.
*   **Características**: Extremadamente lentas (segundos por acción), frágiles (dependen de tiempos de renderizado, red, selectores). Deben ser muy pocas, solo los flujos críticos de negocio (*happy paths*, compra, login, registro).
*   **Ejemplo**: Abrir navegador, ir a la tienda, buscar un producto, añadirlo al carrito, hacer checkout y verificar el resumen de pedido.

## Variantes modernas

*   **Testing Trophy (Kent C. Dodds)**: Enfatiza las pruebas de integración estáticas (con React Testing Library) por sobre las unitarias puras. Para un SDET en frontend, el trofeo invierte un poco la pirámide.
*   **Honeycomb (Spotify)**: Para sistemas con muchos microservicios y pocas UI, se enfoca en pruebas de integración entre servicios, endpoints y contratos.

> [!TIP]
> **Principio común**: Aumentar la confianza reduciendo el costo y el tiempo de feedback. Un SDET siempre está empujando el testing hacia las capas más bajas.

## Cómo aplica el SDET la pirámide

1.  **Audita la cobertura actual**: ¿hay demasiadas pruebas UI y pocas de API? Propone migrar esos escenarios a la capa de servicio.
2.  **Diseña el framework** para que escribir pruebas de integración sea tan fácil como escribir unitarias (patrones reusables, clientes API preconfigurados).
3.  **Implementa la suite de regresión UI** solo con *smoke tests* (pruebas de humo) que validen que todo el sistema en conjunto funciona, y mueve las regresiones detalladas a servicios.

---

| Anterior | Inicio | Siguiente |
| :------- | :----: | :-------- |
| ⏪ [Diferencias entre roles](02-Diferencias-roles.md) | [Índice](01-Que-es-SDET.md) | [Ciclo de vida del software](04-Ciclo-vida-software.md) ⏩ |

