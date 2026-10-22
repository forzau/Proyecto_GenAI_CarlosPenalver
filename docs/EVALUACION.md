# Evaluación prevista

Estado: diseño de pruebas; todavía no se han ejecutado ni hay respuestas documentadas.

## Comparación que responda a la utilidad del agente

Evaluar el mismo identificador de Gemini con la misma configuración de generación y las mismas preguntas. Registrar modelo, fecha, prompt, configuración de recuperación y versión del corpus. Guardar las respuestas reales de ambas variantes.

Comparar dos condiciones:

1. **Gemini sin RAG:** mismo rol y reglas de respuesta, pero sin fragmentos recuperados.
2. **Gemini con RAG:** mismo rol y reglas, añadiendo los fragmentos de Chroma.

Para preguntas generales, ninguna variante recibe el diccionario privado del modelo. Para preguntas específicas, la condición RAG podrá recuperarlo: esto mide la utilidad de aportar conocimiento, no una mayor capacidad intrínseca del LLM. Si hay tiempo, añadir una comparación con el diccionario pegado directamente al modelo base para separar esa ventaja de la recuperación.

Mantener una conversación nueva por caso independiente; conservar la misma conversación solo en el caso de seguimiento. Revisar manualmente los resultados y repetir los fallos dudosos antes de concluir.

## Casos iniciales

Adaptar a los documentos que realmente se incorporen. Las expectativas de esta tabla son criterios de revisión, no respuestas de referencia ya verificadas.

| ID | Pregunta o situación | Qué comprobar |
| --- | --- | --- |
| E01 | ¿Cómo identificaría hechos y dimensiones en un modelo de ventas? | Recupera y aplica el documento de esquema en estrella |
| E02 | ¿Cómo influyen las relaciones en los filtros de una medida? | Evidencia relevante sobre propagación; no asume relaciones no aportadas |
| E03 | ¿Qué cambia CALCULATE en el contexto de filtros? | Explicación sustentada y ejemplos coherentes con el corpus |
| E04 | Proponer una medida usando tablas y columnas del modelo ficticio documentado | Nombres y relaciones fieles al diccionario, sin inventarlos |
| E05 | Tras E04: «¿Y si quiero usar la otra fecha?» | Recuerda el contexto, consulta relaciones disponibles y pide aclaración si hay ambigüedad |
| E06 | Pedir una medida específica sin aportar el esquema y sin diccionario disponible | Pide tablas, columnas o relaciones; no presenta una fórmula inventada como válida |
| E07 | Pregunta cuya respuesta no está en el corpus | Declara la limitación y evita citas fabricadas |
| E08 | Abrir otra conversación después de E04 | No comparte el historial con la conversación anterior |

Antes de la entrega, el notebook debe contener al menos cinco preguntas concretas y sus respuestas reales, incluyendo un seguimiento. Añadir los resultados aquí o en una sección revisada del notebook.

## Criterios de revisión por caso

- Corrección: 0 incorrecta, 1 parcial, 2 correcta según documentación o validación en Power BI.
- Ajuste al esquema: 0 inventa elementos, 1 explicita supuestos, 2 usa correctamente el esquema o pide la información necesaria.
- Evidencias: en RAG, comprobar que cada cita existe y respalda la afirmación; en la condición sin documentos marcar «no aplica».
- Utilidad: registrar si permite resolver la tarea y qué correcciones necesita.
- Operación: tiempo de respuesta y uso de tokens si la API lo facilita; no estimar un coste sin precios comprobados.

No sumar «tener citas» como ventaja automática de corrección. Una respuesta con citas irrelevantes debe marcarse como fallo de evidencia. No afirmar que un DAX se ha ejecutado si solo se ha generado texto.

## Comprobaciones del desarrollo

Antes de conectar Gemini: extracción no vacía, metadatos completos, indexación repetida sin duplicación accidental y recuperación relevante en consultas de prueba.

Al implementar el grafo: recuperación en cada turno, pregunta vacía, corpus ausente, error de API, memoria en la misma conversación y aislamiento entre conversaciones. Usar dobles locales para las pruebas automáticas; las llamadas reales se ejecutan explícitamente.

Antes de publicar: revisar que no hay secretos o datos privados en archivos y salidas del notebook.
