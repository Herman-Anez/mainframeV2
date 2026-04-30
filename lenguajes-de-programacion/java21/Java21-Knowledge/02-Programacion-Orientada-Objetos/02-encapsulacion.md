# ENCAPSULACIÓN
1. Principio de encapsulación

Consiste en ocultar el estado interno de un objeto y solo permitir su manipulación a través de una interfaz pública de métodos. Reduce el acoplamiento y facilita el mantenimiento.
2. Modificadores de acceso en Java

Java provee cuatro niveles de acceso, de más restrictivo a más abierto:
Modificador	Clase	Paquete	Subclase	Mundo
private	✔
(sin modificador)	✔	✔
protected	✔	✔	✔
public	✔	✔	✔	✔

    private solo dentro de la misma clase. Ideal para campos.

    Package‑private accesible desde clases del mismo paquete. Útil para clases y métodos internos al módulo/paquete.

    protected añade acceso desde subclases, incluso si están en distinto paquete. Común en métodos pensados para herencia.

    public para la API pública. Usar con moderación.

3. Uso de getters y setters

Para exponer campos de manera controlada se definen métodos:
```java
public class Cuenta {
    private double saldo;
    public double getSaldo() { return saldo; }
    public void depositar(double monto) {
        if (monto > 0) saldo += monto;
    }
}
```

Los records generan automáticamente métodos getter con el nombre del componente, pero no setters porque son inmutables.
4. Objetos inmutables

Un objeto inmutable no puede cambiar su estado una vez construido. Claves:

    Todos los campos final.

    La clase final o no proporciona métodos que modifiquen el estado.

    No exponer referencias mutables; devolver copias defensivas.

Ejemplo típico: String, BigInteger, y los record. La inmutabilidad facilita la programación concurrente.
5. Encapsulación reforzada con módulos (JPMS)

Desde Java 9, el sistema de módulos permite encapsular paquetes completos incluso del mismo módulo si no se exportan explícitamente en module-info.java:
```java
module mi.modulo {
    exports com.mi.paquete.api;
    // com.mi.paquete.internal no es accesible desde fuera
}
```

Esto añade una capa de encapsulación por encima de los modificadores de acceso tradicionales.
6. Encapsulación en records

Los registros son inmutables, pero la encapsulación se mantiene: no se pueden modificar los campos, aunque los getter exponen los valores. Se pueden definir métodos adicionales y el constructor canónico puede validar o normalizar los datos mediante el constructor compacto:
```java
public record Persona(String nombre, int edad) {
    public Persona {   // compacto, sin parámetros
        if (edad < 0) throw new IllegalArgumentException(...);
    }
}
```

Los campos siguen siendo private final y solo se accede a través de los getter automáticos.
