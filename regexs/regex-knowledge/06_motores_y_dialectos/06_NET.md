# NET.md
## El motor de .NET

El espacio de nombres `System.Text.RegularExpressions` de .NET (C#, VB.NET, PowerShell) implementa uno de los motores de regex más potentes y flexibles. Data de los primeros Framework y ha sido mejorado en .NET Core y .NET 5+.

### Características exclusivas

*   **Lookbehind completamente variable** sin restricciones de longitud.
*   **Grupos balanceados**: permiten emparejar construcciones anidadas arbitrarias (paréntesis, tags) sin recursión.
*   **Agrupaciones con mismo nombre**: varios grupos pueden tener el mismo nombre y capturar múltiples valores a lo largo de la cadena.
*   **Ejecución de derecha a izquierda** con `RegexOptions.RightToLeft`.
*   **Soporte completo para Unicode**, propiedades, scripts.
*   **Condicionales** `(?(cond)si|no)`.
*   **Grupos atómicos** `(?>...)`.
*   **Cuantificadores posesivos** (solo en algunas versiones, aunque `*+` es raro; el grupo atómico suple).
*   **Sustitución dinámica** con `MatchEvaluator`.

### Lookbehind variable

En .NET, cualquier patrón puede aparecer dentro de un lookbehind. El motor retrocede desde la posición actual hacia la izquierda aplicando el patrón.
```csharp
Regex.Match("123abc", @"(?<=\d{2,})abc"); // éxito, "abc" precedido por al menos 2 dígitos
```

### Grupos balanceados

Son la joya de .NET para parsear anidamientos. Utilizan los nombres open y close con una pila.

**Sintaxis básica:**
*   `(?<nombre>)` apila una captura.
*   `(?<-nombre>)` desapila.
*   `(?(nombre)(?!))` verifica si la pila está vacía.

#### Ejemplo: paréntesis balanceados en una cadena
```csharp
string pattern = @"
  \(
  (?>
      [^()]+
    | \( (?<depth>)
    | \) (?<-depth>)
  )*
  (?(depth)(?!))
  \)
";
Match m = Regex.Match("(a (b) c)", pattern, RegexOptions.IgnorePatternWhitespace);
```
*   `\(` y `\)` delimitan.
*   `[^()]+` secuencias sin paréntesis.
*   `\( (?<depth>)` empuja en la pila.
*   `\) (?<-depth>)` saca.
*   `(?(depth)(?!))` falla si la pila no está vacía.

### Grupos con el mismo nombre y capturas múltiples

En .NET, `(?<num>\d+)` aplicado varias veces conserva todas las capturas bajo el mismo nombre, accesibles vía `match.Groups["num"].Captures`.
```csharp
Match m = Regex.Match("12,34,56", @"(?<num>\d+)(?:,(?<num>\d+))*");
foreach (Capture cap in m.Groups["num"].Captures)
    Console.WriteLine(cap.Value); // 12, 34, 56
```

### Condicionales

Soportan condiciones basadas en si un grupo capturó, o si una aserción se cumple.
```csharp
// Coincide con "abc" o "ABC" según un prefijo
Regex.Replace("prefix:abc", @"(prefix:)?(?(1)[A-Z]+|[a-z]+)", "...");
```
*Si existe el grupo 1, exige mayúsculas; si no, minúsculas.*

### Flags y opciones

*   `RegexOptions.IgnoreCase`
*   `RegexOptions.Multiline`
*   `RegexOptions.Singleline` (dotall)
*   `RegexOptions.IgnorePatternWhitespace` (modo verboso)
*   `RegexOptions.ExplicitCapture` (solo grupos con nombre capturan)
*   `RegexOptions.RightToLeft` (empieza desde el final de la cadena, útil para búsquedas desde atrás)
*   `RegexOptions.ECMAScript` (comportamiento compatible con JavaScript, desactiva algunas extensiones)

### Reemplazos con MatchEvaluator

Permite usar una lambda para decidir la cadena de reemplazo en base al Match.
```csharp
Regex.Replace("hola MUNDO", @"\w+", m => m.Value.ToUpper()); // "HOLA MUNDO"
```

### Limitaciones

*   No tiene recursión explícita `(?R)`, pero los grupos balanceados cubren la mayoría de casos de anidamiento.
*   La sintaxis de posesivos `(*+)` es aceptada en .NET Core/.NET 5+, aunque no está documentada en todas partes; el grupo atómico es preferible.
*   El motor es backtracking y sufre los mismos riesgos de patrones catastróficos.

### Ejemplo práctico completo

Extraer todas las urls de un texto, evitando las que están en etiquetas HTML:
```csharp
string pattern = @"<a\s[^>]*>.*?</a>(*SKIP)(*FAIL)|https?://[^\s""']+";
// Sin embargo (*SKIP) no existe en .NET. Alternativa con balanceo o MatchEvaluator complejo.
```

> [!NOTE]
> En .NET, para saltar regiones se suele usar un enfoque de split o `Regex.Replace` con un evaluador.

---

### 📖 Temas relacionados
| Archivo | Descripción |
| :--- | :--- |
| [01_comparativa_general.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/06_motores_y_dialectos/01_comparativa_general.md) | Comparativa entre motores |
| [05_Java.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/06_motores_y_dialectos/05_Java.md) | Regex en Java |
| [02_PCRE.md](file:///home/hermandev/Documents/proyectos/1Profecional/mainframeV2/regexs/regex-knowledge/06_motores_y_dialectos/02_PCRE.md) | Detalles de PCRE |
