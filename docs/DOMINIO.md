# Propuesta: asistente de DAX y modelado en Power BI

Estado: propuesta inicial que ha interesado al alumno. Confirmar alcance antes de recopilar el corpus.

## Usuario y problema

Una persona que desarrolla informes y necesita entender medidas DAX, contexto de filtros y relaciones. El asistente buscará evidencias y aplicará las explicaciones al esquema que reciba.

## Alcance de una semana

- Modelado en estrella: tablas de hechos, dimensiones y granularidad.
- Relaciones, dirección de filtrado y relaciones activas/inactivas.
- Medidas DAX centradas en CALCULATE y contexto de filtros.
- Un modelo de ventas ficticio con diccionario de tablas, columnas, relaciones y medidas. Se escribirá al desarrollar el corpus; todavía no existe.

Fuera del MVP: administración de Fabric, licencias, gateways, actualización de datos, todo Power Query, conexión a Power BI Service, lectura de PBIX y ejecución o modificación automática de informes.

## Cuándo puede aportar valor frente a un modelo base

1. Consultas sobre el esquema ficticio que Gemini no conoce de antemano.
2. Respuestas respaldadas por fragmentos concretos de documentación seleccionada.
3. Seguimientos que conservan las tablas y restricciones del turno anterior.
4. Reconocer cuándo faltan datos para proponer una medida.

En preguntas generales el modelo base puede ser igual o mejor. El RAG puede recuperar fragmentos irrelevantes o incompletos. La comparación de EVALUACION.md debe reflejar ambos casos; no se asumirá superioridad.

## Caso de uso para la demo

Definir una medida sobre el modelo ficticio, explicar cómo interactúa con sus relaciones y adaptar la medida en un segundo turno. Mostrar la documentación que sustenta la explicación y una consulta cuya respuesta no está en el corpus.

## Decisiones abiertas

- ¿Qué problema de Power BI aparece con más frecuencia en el trabajo del alumno?
- ¿Qué esquema ficticio representa bien ese problema?
- ¿Qué documentos y versiones concretas formarán el corpus?
- ¿Cuál es la fecha y hora exactas de entrega?
- ¿Qué cuota o presupuesto de Gemini estará disponible para las pruebas?
