# Técnicas de diseño de pruebas

Un SDET no solo escribe código, sino que sabe qué probar y cómo seleccionar los casos mínimos que maximizan la cobertura de fallos. Las técnicas abarcan caja negra, caja blanca y basadas en experiencia.

## Técnicas de caja negra (sin ver código)

### 1. Partición de equivalencia (*Equivalence Partitioning*)
Divide los datos de entrada en grupos que se espera se comporten de manera similar. Se prueba un representante de cada partición.
*   **Ejemplo**: Campo "edad" (válidos 0-120). Particiones: números negativos (inválido), 0-120 (válido), >120 (inválido), texto (inválido).

### 2. Análisis de valores límite (*Boundary Value Analysis*)
Complementa la anterior. Los errores suelen ocurrir en los bordes de las particiones.
*   **Ejemplo**: Para rango 0-120, probar: -1, 0, 1, 119, 120, 121.

### 3. Tablas de decisión
Útiles para lógica compleja con combinaciones de condiciones y acciones.
*   **Ejemplo**: Descuento según tipo de cliente (VIP/Regular) y monto de compra (>100, ≤100).

### 4. Transición de estados
Para sistemas que cambian de estado según eventos. Se modelan estados y transiciones para cubrir caminos válidos e inválidos.
*   **Ejemplo**: Ciclo de vida de un pedido (Creado → Pagado → Enviado).

### 5. Pruebas de pares (*Pairwise testing*)
Garantiza que cada par de valores de parámetros se prueba al menos una vez, reduciendo el número total de combinaciones.
*   **Herramientas**: PICT (Microsoft), ACTS.

## Técnicas de caja blanca (ver el código)

### Cobertura de sentencias, ramas y caminos
Asegurar que la suite unitaria ejecuta todas las líneas (sentencias) y todas las decisiones verdadero/falso (ramas). El SDET revisa estas métricas con herramientas como **JaCoCo** o **Istanbul**.

### Pruebas de mutación
Introducen pequeños cambios (mutantes) en el código fuente para verificar si las pruebas los detectan. Si un mutante sobrevive, las pruebas no son robustas.
*   **Herramientas**: PIT (Java), Stryker (JS/.NET).

## Técnicas basadas en la experiencia

### Testing exploratorio
Aprendizaje simultáneo, diseño y ejecución de pruebas. El SDET lo usa para identificar riesgos no contemplados por la automatización. Se suele gestionar con **SBTM** (*Session-Based Test Management*).

### Pruebas basadas en riesgos
Priorizar qué probar según el impacto y probabilidad de fallo. Ayuda al SDET a decidir qué automatizar primero.

## Diseño de casos con Gherkin (BDD)

El SDET suele ser el facilitador de BDD. Escribe escenarios legibles para el negocio y automáticamente ejecutables.

```gherkin
Scenario: Retirar dinero con saldo suficiente
  Given el cliente tiene una cuenta con saldo 500€
  When retira 200€
  Then el saldo de la cuenta debe ser 300€
  And el cajero debe dispensar 200€
```

## Aplicación práctica para el SDET

Al recibir una historia de usuario, el SDET combina varias técnicas: define particiones de equivalencia, verifica los valores límite, modela la transición de estados si aplica y escribe escenarios BDD para los flujos principales. Luego, codifica esas técnicas en scripts dinámicos y robustos.

---

| Anterior | Inicio | Siguiente |
| :------- | :----: | :-------- |
| ⏪ [Ciclo de vida del software](04-Ciclo-vida-software.md) | [Índice](01-Que-es-SDET.md) | [Buenas prácticas](../02-Programacion/Buenas-practicas/index.md) ⏩ |


