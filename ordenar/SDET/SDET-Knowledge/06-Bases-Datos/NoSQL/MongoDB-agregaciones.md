MongoDB - agregaciones

El pipeline de agregación de MongoDB es extremadamente potente para transformar y resumir datos en el servidor. El SDET lo usa para verificar la salida de estos pipelines cuando la aplicación expone esos datos vía API.

Estructura de un pipeline:
Cada etapa ($match, $group, $sort, $project, $lookup, etc.) procesa los documentos y pasa el resultado a la siguiente.

    $match: Filtrado. Similar a WHERE.
    javascript

    { $match: { status: "PAID", "amount": { $gt: 100 } } }

    $group: Agrupación con acumuladores ($sum, $avg, $push, $addToSet).
    Ejemplo: total de ventas por categoría.
    javascript

    { $group: { _id: "$category", totalSales: { $sum: "$amount" } } }

    $project: Selección de campos, renombrado, creación de campos calculados.
    { $project: { fullName: { $concat: ["$first", " ", "$last"] }, total: 1 } }

    $lookup: Left Outer Join entre colecciones (similar a JOIN SQL).
    javascript

    { $lookup: { from: "customers", localField: "customerId", foreignField: "_id", as: "customer" } }

    Luego se puede $unwind para desanidar.

    $unwind: Descompone un campo array en documentos separados por cada elemento.

    $sort, $limit, $skip: Ordenación y paginación.

Pruebas de agregaciones:

    Se prepara un conjunto de documentos en la colección de pruebas (insertados desde el test o mediante fixtures).

    Se ejecuta la agregación utilizando el driver de MongoDB (collection.aggregate(pipeline)).

    Se verifican los resultados contra los valores esperados.
    javascript

    // Ejemplo con Node.js driver / Jest
    const pipeline = [
      { $match: { year: 2024 } },
      { $group: { _id: "$month", total: { $sum: "$sales" } } }
    ];
    const result = await collection.aggregate(pipeline).toArray();
    expect(result).toEqual(
      expect.arrayContaining([
        expect.objectContaining({ _id: 1, total: 200 }),
        expect.objectContaining({ _id: 2, total: 150 })
      ])
    );

    El SDET aísla estas pruebas usando una instancia de MongoDB en contenedor o bases de datos embebidas (como mongodb-memory-server en Node) que se levantan antes de los tests y se apagan después.

Casos comunes:

    Validar que un endpoint de reporte devuelve exactamente lo que la agregación correspondiente produce.

    Probar la lógica de $lookup cuando hay cambios en esquemas de colecciones relacionadas.

    Asegurar que índices se usan correctamente: aunque no es una prueba funcional, el SDET puede incluir queries con explain("executionStats") para validar que no se pierda rendimiento.

Manejo de datos en MongoDB vs SQL:

    Sin esquemas fijos, las pruebas deben contemplar documentos con campos faltantes. Se añaden documentos que cubran esos casos (campos opcionales en null, arrays vacíos) para que la agregación no rompa.

    Los $facet (sub-pipelines múltiples) se prueban con documentos que aseguren que cada sub-pipeline se ejecuta correctamente.