# 📁 Agrupación y Captura: Grupos Nombrados

## 📌 Concepto

Los **grupos con nombre** permiten asignar un identificador textual a un grupo de captura, en lugar de depender únicamente de su índice numérico. Esto mejora drásticamente la legibilidad del código y hace que las expresiones regulares sean más resistentes a cambios estructurales (como añadir o quitar grupos).

---

## 📌 Variantes de sintaxis según motor

Lamentablemente, no existe un estándar único para definir grupos nombrados, aunque las variantes más comunes son las siguientes:

| Motor / Lenguaje | Sintaxis de definición | Retroreferencia interna | Uso en reemplazo |
| :--- | :--- | :--- | :--- |
| **Python (`re`)** | `(?P<nombre>...)` | `(?P=nombre)` | `\g<nombre>` |
| **PCRE / Perl** | `(?<nombre>...)` o `(?'nombre'...)` | `\k<nombre>` o `\k'nombre'` | `$+{nombre}` (Perl) o `\g<nombre>` |
| **JavaScript (ES2018+)** | `(?<nombre>...)` | `\k<nombre>` | `$<nombre>` |
| **.NET** | `(?<nombre>...)` o `(?'nombre'...)` | `\k<nombre>` | `${nombre}` |
| **Java (Java 7+)** | `(?<nombre>...)` | `\k<nombre>` | `${nombre}` |

> [!NOTE]
> En Python, el módulo estándar `re` solo soporta la sintaxis `(?P<nombre>)`. El módulo externo `regex` soporta tanto la sintaxis de Python como la de PCRE.

---

## 📌 Ejemplo con diferentes sintaxis

### 🔹 Python
```python
import re
patron = r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'
m = re.search(patron, '2024-12-25')

print(m.group('year'))   # '2024'
print(m.group('month'))  # '12'
print(m.group('day'))    # '25'
```

### 🔹 JavaScript
```javascript
let regex = /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/;
let match = regex.exec('2024-12-25');

console.log(match.groups.year);   // '2024'
console.log(match.groups.month);  // '12'
console.log(match.groups.day);    // '25'
```

### 🔹 Java
```java
Pattern p = Pattern.compile("(?<year>\\d{4})-(?<month>\\d{2})-(?<day>\\d{2})");
Matcher m = p.matcher("2024-12-25");

if (m.find()) {
    System.out.println(m.group("year"));  // "2024"
    System.out.println(m.group("month")); // "12"
    System.out.println(m.group("day"));   // "25"
}
```

---

## 📌 Ventajas de los nombres

1.  **Código más legible:** Es mucho más claro leer `m.group('year')` que `m.group(1)`.
2.  **Resistencia a cambios:** Si insertas un nuevo grupo de captura al inicio de la regex, la numeración de los grupos posteriores cambiará, pero las referencias por nombre seguirán funcionando sin cambios en el código.
3.  **Autodocumentación:** El propio patrón describe qué información está intentando extraer, actuando como documentación interna.

---

## 📌 Reglas y compatibilidades

- **Identificadores válidos:** Los nombres deben ser identificadores válidos (letras, dígitos y guiones bajos en la mayoría de motores, y generalmente no pueden empezar por un dígito).
- **Nombres únicos:** Por lo general, no puede haber dos grupos con el mismo nombre dentro del mismo patrón.
    - *Excepción:* Motores como .NET permiten nombres duplicados, compartiendo la captura. En PCRE y JavaScript esto resultará en un error de sintaxis.
- **Retrocompatibilidad:** Los grupos nombrados también conservan su índice numérico; puedes seguir accediendo a ellos mediante números si es necesario.

---

## 📌 Uso en reemplazos

### 🔹 Python
```python
import re
texto = "Juan Perez"
# Intercambiar nombre y apellido usando nombres de grupo
re.sub(r'(?P<nombre>\w+) (?P<apellido>\w+)', r'\g<apellido>, \g<nombre>', texto)
# Resultado: "Perez, Juan"
```

### 🔹 JavaScript
```javascript
let texto = "Juan Perez";
texto.replace(/(?<nombre>\w+) (?<apellido>\w+)/, '$<apellido>, $<nombre>');
// Resultado: "Perez, Juan"
```

---

## 📌 Compatibilidad con cuantificadores y anidamiento

Los grupos con nombre pueden anidarse y combinarse libremente con grupos sin nombre y grupos sin captura. La numeración de todos los grupos (nombrados o no) sigue el orden de apertura de los paréntesis.

> [!TIP]
> Puedes referenciar un grupo por número incluso si tiene un nombre asignado. El nombre es simplemente un alias adicional para facilitar el acceso.

---

| Anterior | Inicio | Siguiente |
| :--- | :---: | ---: |
| [Grupos sin Captura](02_grupos_sin_captura.md) | [Índice](../README.md) | [Retroreferencias](04_retroreferencias.md) |
