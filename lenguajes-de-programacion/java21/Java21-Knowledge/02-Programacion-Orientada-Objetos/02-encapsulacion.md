# Encapsulación

La encapsulación es uno de los pilares de la POO que consiste en ocultar el estado interno de un objeto, exponiendo solo lo necesario a través de una interfaz pública de métodos.

---

## El Principio de Encapsulación

Consiste en ocultar el estado interno de un objeto y solo permitir su manipulación a través de una interfaz pública de métodos. Esto reduce el acoplamiento y facilita enormemente el mantenimiento del código.

---

## Modificadores de Acceso en Java

Java provee cuatro niveles de acceso, desde el más restrictivo hasta el más abierto:

| Modificador | Clase | Paquete | Subclase | Mundo |
| :--- | :---: | :---: | :---: | :---: |
| **`private`** | ✔ | | | |
| **(Sin modificador)** | ✔ | ✔ | | |
| **`protected`** | ✔ | ✔ | ✔ | |
| **`public`** | ✔ | ✔ | ✔ | ✔ |

### Detalles de visibilidad:
- **`private`**: Solo accesible dentro de la misma clase. Es el nivel ideal para los campos (variables de instancia).
- **Package-private (sin modificador)**: Accesible desde cualquier clase del mismo paquete. Útil para clases y métodos internos al módulo.
- **`protected`**: Añade acceso desde subclases, incluso si están en un paquete distinto. Es común en métodos diseñados para ser extendidos.
- **`public`**: Acceso total desde cualquier parte del mundo. Debe usarse con moderación para definir la API pública.

---

## Uso de Getters y Setters

Para exponer campos de manera controlada se definen métodos de acceso y modificación:

```java
public class Cuenta {
    private double saldo;

    public double getSaldo() { 
        return saldo; 
    }

    public void depositar(double monto) {
        if (monto > 0) {
            saldo += monto;
        }
    }
}
```

> [!NOTE]
> Los **registros** (`record`) generan automáticamente métodos getter con el nombre del componente, pero carecen de setters debido a su inmutabilidad.

---

## Objetos Inmutables

Un objeto inmutable es aquel que no puede cambiar su estado una vez construido. Esto es clave para la seguridad y la programación concurrente.

### Claves para la inmutabilidad:
- Declarar todos los campos como `final`.
- Definir la clase como `final` o evitar métodos que modifiquen el estado.
- No exponer referencias mutables; en su lugar, devolver **copias defensivas**.

> [!TIP]
> Ejemplos típicos de inmutabilidad en Java son `String`, `BigInteger` y las clases de tipo `record`.

---

## Encapsulación Reforzada con Módulos (JPMS)

Desde Java 9, el sistema de módulos permite encapsular paquetes completos, incluso si contienen miembros públicos, si no se exportan explícitamente en el archivo `module-info.java`:

```java
module mi.modulo {
    exports com.mi.paquete.api;
    // com.mi.paquete.internal no es accesible desde fuera del módulo
}
```

---

## Encapsulación en Registros (`record`)

Los registros son inmutables por naturaleza, pero mantienen la encapsulación: los campos son `private final` y solo se accede a ellos a través de los getters automáticos. Se puede añadir validación en el **constructor compacto**:

```java
public record Persona(String nombre, int edad) {
    public Persona {   // Constructor compacto, sin parámetros
        if (edad < 0) {
            throw new IllegalArgumentException("La edad no puede ser negativa");
        }
    }
}
```
