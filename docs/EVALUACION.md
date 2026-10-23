# Evaluación prevista

Estado: diseño de pruebas; todavía no se han ejecutado ni hay respuestas documentadas. Los escenarios de piloto serán ficticios salvo que se indique una prueba real en el simulador.

## Comparación frente a Gemini sin RAG

Usar el mismo identificador de Gemini, configuración de generación, rol, reglas de respuesta, preguntas e historial de piloto en ambas variantes. Registrar modelo, fecha, prompt, corpus, filtros y configuración de recuperación.

1. **Gemini sin RAG:** recibe la consulta y el mismo contexto de sesión facilitado por el piloto, sin documentos recuperados.
2. **Gemini con RAG:** recibe lo anterior más fragmentos de Chroma filtrados por simulador y revisados por aplicabilidad.

La memoria debe estar disponible en ambas variantes para evaluar el efecto de RAG. Probar por separado el seguimiento y la recuperación. No ocultar al modelo base datos del piloto que sí reciba el agente. Si hay tiempo, añadir una comparación pegando el mismo material documental al modelo base.

Mantener una conversación nueva por caso independiente; conservarla solo en los seguimientos. Revisar manualmente las respuestas y repetir los fallos dudosos. No indexar las respuestas de referencia de evaluación como parte del corpus.

## Primeras preguntas documentales de LMU

El alumno solo ha jugado LMU, principalmente GT3, y recuerda dificultad con el sobreviraje sin identificar coche, versión o fase de curva. Las preguntas L01–L05 son candidatas documentales propuestas para el proyecto; L06 utiliza su relato incompleto. No hay resultados del agente. Podremos preparar criterios de corrección tras revisar los artículos; las tablas e imágenes siguen pendientes de comprobación.

| ID | Pregunta candidata | Fuente de partida y revisión necesaria |
| --- | --- | --- |
| L01 | ¿El control de tracción se configura como una ayuda global o dentro del coche en LMU? | LMU03; verificar explicación y límites de aplicabilidad |
| L02 | ¿Qué diferencia hay entre Traction Control, Power Cut y Slip Angle? | LMU03; revisar texto y capturas, sin inventar escalas para un coche no identificado |
| L03 | Tras L02: «¿Cuál de esos controles debo consultar si quiero entender cuánto se reduce la potencia?» | LMU03; seguimiento documental para comprobar referencia al turno anterior |
| L04 | ¿La explicación del ABS para LMGT3 se puede aplicar a cualquier categoría? | LMU04; revisar alcance y distinguir documentación disponible de inferencias |
| L05 | ¿Qué diferencias de ajuste describe la guía entre sus dos LMP3? | LMU02; caso complementario, no prioritario para la experiencia GT3 del alumno; no extrapolar entre categorías |
| L06 | «Recuerdo conducir GT3 en LMU: sobreviraban con facilidad y me costaba recuperarlos» | Relato histórico del alumno, no evidencia técnica: preguntar por coche, versión y fase relevante; no asumir causa, prescribir TC ni inventar datos. LMU03/LMU04 solo se consultarán según el contexto que llegue a aclararse |

No habrá respuestas de referencia hasta contrastarlas con las fuentes. Estas preguntas permiten arrancar la validación de RAG y memoria sin rodar. Los escenarios de síntomas de la tabla siguiente se mantendrán como casos hipotéticos y se concretarán con la documentación aplicable.

## Casos iniciales

Adaptar coche, versión y condiciones al corpus final. Las expectativas son criterios de revisión, no recomendaciones técnicas ni respuestas ya verificadas.

| ID | Pregunta o situación | Qué comprobar |
| --- | --- | --- |
| E01 | «El coche se va de morro, ¿qué necesitas saber?» | Solicita contexto relevante sin inventar simulador, coche o fase de curva; puede explicar conceptos generales |
| E02 | Caso de iRacing: coche y condiciones aportados, subviraje en una fase concreta | Recupera fuentes aplicables y propone una prueba principal razonada, sin parámetros inexistentes |
| E03 | Caso de ACC: consulta de neumáticos con coche y versión identificados | Verifica aplicabilidad y unidades; no usa cifras de iRacing o LMU ni toma una guía histórica como vigente por defecto |
| E04 | Caso de LMU: problema de comportamiento de un coche documentado | Fundamenta la respuesta en material de LMU y no extrapola entre categorías sin evidencia |
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

- Corrección: 0 incorrecta, 1 parcial, 2 coherente con documentación aplicable.
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
