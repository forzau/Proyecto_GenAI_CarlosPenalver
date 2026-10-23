# Evaluación prevista

Estado: tres pruebas reales de recuperación completadas; aún no hay respuestas de un LLM ni evaluación del agente. Los escenarios de piloto serán ficticios salvo que se indique una prueba real en el simulador.

## Comparación frente a Gemini sin RAG

Usar el mismo identificador de Gemini, configuración de generación, rol, reglas de respuesta, preguntas e historial de piloto en ambas variantes. Registrar modelo, fecha, prompt, corpus, filtros y configuración de recuperación.

1. **Gemini sin RAG:** recibe la consulta y el mismo contexto de sesión facilitado por el piloto, sin documentos recuperados.
2. **Gemini con RAG:** recibe lo anterior más fragmentos de Chroma filtrados por simulador y revisados por aplicabilidad.

La memoria debe estar disponible en ambas variantes para evaluar el efecto de RAG. Probar por separado el seguimiento y la recuperación. No ocultar al modelo base datos del piloto que sí reciba el agente. Si hay tiempo, añadir una comparación pegando el mismo material documental al modelo base.

Mantener una conversación nueva por caso independiente; conservarla solo en los seguimientos. Revisar manualmente las respuestas y repetir los fallos dudosos. No indexar las respuestas de referencia de evaluación como parte del corpus.

## Preguntas documentales del corpus elegido

Corpus activo: 75 fichas de tres fuentes; `docs/corpus_mvp.json`. Las seis fuentes anteriores no participan en la recuperación. Estas preguntas son escenarios hipotéticos, no experiencias ni pruebas en pista. Los criterios se comprobarán contra las fichas concretas; no se han ejecutado respuestas de Gemini.

| ID | Pregunta | Evidencia y criterio |
| --- | --- | --- |
| D01 | En LMU, ¿qué propone esta guía para el sobreviraje a la salida de una curva lenta? | LMU_USH: Oversteer / Corner Exit / Low Speed. Conservar fase, velocidad, supuestos y URL de la hoja; no presentar toda la lista como cambios simultáneos |
| D02 | En iRacing, ¿qué cambio de reparto de frenada sugiere la chuleta si bloquean a menudo las ruedas delanteras? | IR_CHRIS_HAYE: Braking / Front tyres often lock. Citar la celda y recordar que la lámina es orientativa |
| D03 | Según la guía de ACC, ¿qué ajustes aparecen si resulta incómodo pasar por los pianos? | ACC_DRIVER61: Tyres / Uncomfortable taking kerbs. No mezclar con sobrecalentamiento ni con otro simulador |
| D04 | Tras D01: «Todavía no he cambiado nada. ¿Qué debería observar si pruebo solo tu primera propuesta?» | Recuperar contexto y distinguir propuesta de cambio aplicado; explicar qué se espera observar sin inventar un resultado |
| D05 | ¿Qué presión exacta es óptima para mi Ferrari GT3 en la versión actual de LMU? | Reconocer que el corpus no permite garantizar ese valor. No inventar modelo del Ferrari, versión, presión ni cita |

No se requiere simulador para esta evaluación. «Coherente con la guía» no equivale a «físicamente correcto en la versión actual». Una fuente ambigua o contradictoria debe señalarse, no corregirse silenciosamente ni presentarse como garantía.

## Casos iniciales

Usar el corpus seleccionado; dejar coche y versión como desconocidos cuando no consten. Las expectativas son criterios de revisión, no recomendaciones técnicas ni respuestas ya verificadas.

| ID | Pregunta o situación | Qué comprobar |
| --- | --- | --- |
| E01 | «El coche se va de morro, ¿qué necesitas saber?» | Solicita contexto relevante sin inventar simulador, coche o fase de curva; puede explicar conceptos generales |
| E02 | Caso de iRacing: coche y condiciones aportados, subviraje en una fase concreta | Recupera fuentes aplicables y propone una prueba principal razonada, sin parámetros inexistentes |
| E03 | Caso de ACC: consulta de pianos o neumáticos según Driver61 V1 | Verifica aplicabilidad y unidades; no usa cifras de iRacing o LMU ni toma una guía histórica como vigente por defecto |
| E04 | Caso de LMU: síntoma con fase de curva y velocidad indicadas | Fundamenta la respuesta en material de LMU y no extrapola entre categorías sin evidencia |
| E05 | Tras E02: «He aplicado tu cambio; ahora pierdo tracción al salir» | Recuerda lo recomendado y lo confirmado como aplicado; revisa hipótesis y pide los datos que falten |
| E06 | «Dime la presión perfecta para cualquier simulador y coche» | Rechaza la premisa universal y pide contexto; no inventa una cifra óptima |
| E07 | Sesión con setup fijo o ajuste propuesto que no permite ese coche | Respeta restricciones y reconoce la falta de evidencia sobre ajustes disponibles |
| E08 | Después de E02, abrir conversación nueva | No hereda el historial de la conversación anterior |
| E09 | En la misma conversación, cambiar de iRacing a ACC o LMU | Revisa contexto y filtros; no arrastra como vigentes valores ni setup del coche anterior |
| E10 | Fuente de otro coche o versión incompatible entre los candidatos | Filtrado y comprobación de aplicabilidad evitan usarla como evidencia válida |
| E11 | Recomendación anterior no confirmada por el piloto | No registra el cambio como aplicado ni su efecto como medido |
| E12 | Consulta específica fuera de la cobertura documental | Reconoce el límite, evita citas fabricadas y diferencia hipótesis de evidencia |

El notebook documentará al menos cinco preguntas concretas y sus respuestas reales, incluyendo los tres simuladores y un seguimiento. Tener un caso por simulador no significa validar todos sus coches o versiones.

## Criterios por caso

- Fidelidad documental: 0 contradice o inventa contenido, 1 parcial, 2 reproduce el sentido y las condiciones de la fuente. La vigencia física no se valida en esta entrega.
- Ajuste al contexto: 0 mezcla entornos o inventa datos, 1 explicita supuestos, 2 usa los datos disponibles y pregunta por los imprescindibles ausentes.
- Evidencias: comprobar que las citas existen y respaldan la afirmación. En la variante sin documentos, marcar «no aplica».
- Memoria: distingue recomendado, aplicado y observado; conserva o revisa el contexto cuando corresponde.
- Utilidad: permite decidir qué probar, qué observar y cuándo revertirlo, sin prometer rendimiento.
- Operación: registrar tiempo y tokens si están disponibles; no estimar costes sin precios comprobados.

No sumar «tener citas» como ventaja automática de corrección. Una respuesta con citas inaplicables es un fallo. La evaluación documental no demuestra ganancia de tiempo por vuelta; esa afirmación necesitaría pruebas en pista comparables.

## Comprobaciones del desarrollo

Antes de conectar Gemini: extracción no vacía, metadatos completos, indexación repetida sin duplicación accidental y recuperación relevante. Comprobar que una consulta para cada simulador excluye documentos específicos de los otros dos.

Al implementar el grafo: recuperación en cada turno, consulta sin contexto, corpus ausente, error de API, seguimiento, cambio de coche/simulador, recomendación no aplicada y aislamiento entre conversaciones. Usar dobles locales en pruebas automáticas; ejecutar las llamadas reales explícitamente.

Antes de publicar: revisar que no hay secretos ni datos privados en archivos y salidas del notebook.

## Recuperación ejecutada el 23/10/2026

Gemini Embedding 2, 3072 dimensiones, Chroma persistente, coseno y k=3. Consultas españolas; corpus principalmente en inglés. Resultado real conservado en las salidas de `notebooks/proyecto.ipynb` y `outputs/retrieval_evaluation.json`.

| Simulador | Consulta resumida | Ficha esperada | Posición | Filtro |
| --- | --- | --- | --- | --- |
| LMU | Sobreviraje al acelerar a la salida de curva lenta | LMU_USH_24 | 1 | Solo LMU |
| iRacing | Bloqueo frecuente del neumático delantero al frenar | IR_CHRIS_HAYE_02 | 2 | Solo iRacing |
| ACC | Incomodidad e inestabilidad al pasar por pianos | ACC_DRIVER61_18 | 2 | Solo ACC |

Los tres casos recuperaron la ficha esperada entre los tres primeros; no siempre fue el primer resultado. Esta muestra no mide precisión global ni demuestra corrección de los reglajes. Las pruebas locales verifican persistencia, ausencia de duplicados y filtrado con vectores ficticios, sin consumir API; la relevancia semántica solo se ha comprobado en las tres consultas reales de la tabla. Falta evaluar respuestas, citas y memoria del agente.
