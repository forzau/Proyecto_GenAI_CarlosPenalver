# Evaluación prevista

Estado: cinco casos D01–D05 con respuestas reales, cubriendo LMU, iRacing, ACC, seguimiento y presión exacta no disponible; además se conserva un seguimiento aplicado. Chat en notebook y 31 pruebas locales. Desde el 26/10 también hay clasificación automática y 15 casos conversacionales reales; ver el apartado siguiente. La revisión documental es parcial. La comparación con Gemini sin RAG se descartó por decisión del alumno el 24/10/2026; no es un requisito del enunciado. Los escenarios de piloto son ficticios salvo que se indique una prueba real en el simulador.

## Enrutamiento automático del 26/10/2026

Grafo `START → clasificar → [lmu, iracing, acc, distinto] → END`, sin selección manual. 36 pruebas locales superadas y arranque de todas las celdas de código en un kernel Jupyter real, con `/salir` y llamadas a LLM/embeddings bloqueadas: cero llamadas durante el arranque.

Evaluación real explícita: 15 casos finales con sus comprobaciones superadas. R01/R14 preguntan por el simulador sin inferirlo del Ferrari/Spa; R02 aclara LMU conservando el síntoma; R03 mantiene contexto; R04/R05 cambian a ACC con confirmación y sin reglajes LMU; R06/R07 proponen iRacing y cancelan; R08 reconduce; R09 atiende iRacing; R10/R11 orientan sobre Automobilista 2 sin Chroma; R12 distingue Assetto Corsa de ACC; R13 pide desambiguar; R15 conserva ACC ante una negación de cambio. Esto acredita solo lo observado en esta muestra.

Hubo un `GoogleAPIError` en la generación de R11. Se conserva el intento y se reanudó solo desde ese caso, restaurando mensajes y contexto de los resultados previos. Se completaron los pendientes. No se cambió de modelo. Consumo: **25 llamadas al modelo**, **5 embeddings de consulta**, **0 embeddings del corpus**; **31.026 tokens de entrada y 3.254 de salida comunicados**. El consumo del intento fallido puede no estar comunicado y la facturación real no se conoce. No se reindexó ni se modificó el corpus.

El clasificador y el prompt especializado se mantuvieron durante la pasada. En la reanudación, las envolturas de las ramas pasaron de lambda a funciones con nombre y el prompt de otros simuladores se reforzó para priorizar observación/conducción sin prescribir reglajes específicos cuando falta coche. El informe conserva las huellas iniciales y por intento; no se trata de una comparación controlada de prompts.

**Fidelidad parcial:** R02/R03 añaden mecanismos y efectos en otras fases no respaldados; R05/R15 desarrollan física no descrita en la celda ACC y omiten su antigüedad V1; R15 propone dos variables inicialmente. R09 acierta el sentido del reparto pero añade explicaciones. R10 dio una orientación de diferencial y transferencia cuestionable; tras reforzar el prompt, R11/R12 priorizan investigación pero siguen sin validación técnica y pueden ser demasiado categóricos. Tener ruta correcta o citas válidas no resuelve estos límites.

Esa pasada y sus revisiones se conservan en el informe; el alumno pidió después retirar las transcripciones del notebook para aligerarlo. Informe privado: `outputs/routing_evaluation_2026-10-26.json`. `scripts/evaluate_routing.py` no usa API sin `--run`; `--resume` continúa pendientes conservando intentos. Los apartados siguientes describen propuestas descartadas y etapas históricas del 23/24 de octubre.

## Propuesta de comparación descartada

La metodología siguiente se conserva como antecedente; no es una tarea pendiente ni forma parte de la entrega acordada.

Usar el mismo identificador de Gemini, configuración de generación, rol, reglas de respuesta, preguntas e historial de piloto en ambas variantes. Registrar modelo, fecha, prompt, corpus, filtros y configuración de recuperación.

1. **Gemini sin RAG:** recibe la consulta y el mismo contexto de sesión facilitado por el piloto, sin documentos recuperados.
2. **Gemini con RAG:** recibe lo anterior más fragmentos de Chroma filtrados por simulador y revisados por aplicabilidad.

La memoria debe estar disponible en ambas variantes para evaluar el efecto de RAG. Probar por separado el seguimiento y la recuperación. No ocultar al modelo base datos del piloto que sí reciba el agente. Si hay tiempo, añadir una comparación pegando el mismo material documental al modelo base.

Mantener una conversación nueva por caso independiente; conservarla solo en los seguimientos. Revisar manualmente las respuestas y repetir los fallos dudosos. No indexar las respuestas de referencia de evaluación como parte del corpus.

## Preguntas documentales del corpus elegido

Corpus activo: 75 fichas de tres fuentes; `docs/corpus_mvp.json`. Las seis fuentes anteriores no participan en la recuperación. Estas preguntas son escenarios hipotéticos, no experiencias ni pruebas en pista. Los cinco casos y un seguimiento aplicado se han ejecutado con Gemini. Se reutilizaron búsquedas y respuestas previas cuando procedía, con la procedencia registrada. Los criterios se comprueban contra las fichas concretas.

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

Gemini Embedding 2, 3072 dimensiones, Chroma persistente, coseno y k=3. Consultas españolas; corpus principalmente en inglés. Resultado real conservado en `outputs/retrieval_evaluation.json` y resumido en esta tabla. La evaluación se ha trasladado a `scripts/evaluate_retrieval.py`, fuera del notebook; no se ha repetido la API por este cambio.

| Simulador | Consulta resumida | Ficha esperada | Posición | Filtro |
| --- | --- | --- | --- | --- |
| LMU | Sobreviraje al acelerar a la salida de curva lenta | LMU_USH_24 | 1 | Solo LMU |
| iRacing | Bloqueo frecuente del neumático delantero al frenar | IR_CHRIS_HAYE_02 | 2 | Solo iRacing |
| ACC | Incomodidad e inestabilidad al pasar por pianos | ACC_DRIVER61_18 | 2 | Solo ACC |

Los tres casos recuperaron la ficha esperada entre los tres primeros; no siempre fue el primer resultado. Esta muestra no mide precisión global ni demuestra corrección de los reglajes. Las pruebas locales verifican persistencia, ausencia de duplicados y filtrado con vectores ficticios, sin consumir API; la relevancia semántica solo se ha comprobado en las tres consultas reales de la tabla. Falta evaluar respuestas, citas y memoria del agente.

## Primer caso del agente (24/10/2026)

Consulta D01: «En LMU, tengo sobreviraje al acelerar a la salida de una curva lenta. ¿Qué propone la guía?». Modelo `gemini-3.1-flash-lite`, temperatura 1.0, máximo 1800 tokens de salida, k=3, filtro LMU y colección `simracing_1809b2209d21ea5366b5`. Sin memoria. Corpus sin cambios.

El notebook se ejecutó con un kernel real. Dos pasadas sobre el mismo caso: dos embeddings de consulta y dos generaciones; no son dos casos independientes ni cinco respuestas de evaluación. Los informes privados conservan modelo, fecha, huellas de corpus y prompt, fragmentos, respuesta y tokens. Las 75 fichas no se reindexaron.

| Pasada | Revisión documental | Tokens entrada / salida |
| --- | --- | --- |
| Inicial | Cita existente y ajuste principal respaldado por `LMU_USH_24`, pero añade un desplazamiento del equilibrio aerodinámico que esa ficha no explica y omite el supuesto de trazada correcta. Se revisa el prompt. | 1859 / 488 |
| Con prompt revisado | Cita `LMU_USH_24`, atribuye la explicación a la guía, explicita el supuesto de trazada correcta y propone aumentar la altura delantera como prueba principal. No repite la explicación aerodinámica añadida. | 2009 / 450 |

Las dos respuestas se conservan en `outputs/agent_smoke_initial.json` y `outputs/agent_smoke.json` (fuera de Git); la copia del notebook anterior a la revisión de voz está en `outputs/proyecto_antes_estilo.ipynb`. La ficha citada se ha comparado con la segunda respuesta. La condición de revertir si empeora el giro a la entrada no aparece en esa ficha: es un criterio observacional propuesto por el modelo, no una afirmación documental validada. La fidelidad sigue necesitando evaluación más amplia; tener un ID válido no garantiza el respaldo de cada frase.

En esas primeras pasadas, diez pruebas locales sin API cubrían corpus, recuperación y límites del grafo. No había memoria ni comparación con el modelo base. Son comprobaciones funcionales con dobles locales, no pruebas de corrección de Gemini. No se conoce la facturación efectiva y no se ha modificado la cuenta.

## Revisión de voz (24/10/2026)

El alumno pidió una voz más propia de un ingeniero, evitando la atribución repetitiva «según la guía». El prompt conserva respaldo y citas, pero integra la evidencia en recomendaciones directas, formula las causas como hipótesis y limita las advertencias a lo que afecte a la decisión.

Se reutilizaron exactamente la pregunta D01 y los tres fragmentos de la recuperación real anterior. Una nueva generación con `gemini-3.1-flash-lite`, temperatura 1.0 y máximo 1800 tokens, sin consulta de embeddings ni evaluación nueva de la recuperación. Uso: 2394 tokens de entrada y 325 de salida. Resultado e información de procedencia en `outputs/agent_style.json`; respuesta real guardada en Markdown en la sección 4 del notebook. Las celdas de código se dejaron sin ejecutar para el prompt actualizado.

La nueva respuesta usa «Empezaría por…» y no repite «según la guía». Cita `LMU_USH_24` y propone reducir la rigidez de la barra estabilizadora trasera; esa opción y la alternativa de bloqueo de potencia figuran en la ficha. Conserva el supuesto de trazada correcta y pregunta si el ajuste está permitido. La mejora de tracción longitudinal es una interpretación cualitativa de la explicación sobre ablandar la suspensión trasera, no una medición ni una garantía. La propuesta principal cambia respecto a las pasadas anteriores: no se ha demostrado consistencia al priorizar ajustes.

Esta comprobación evalúa el cambio de voz en un solo caso. No demuestra mayor conocimiento del dominio ni completa los cinco casos de entrega. La revisión documental y la de estilo se registran por separado.

## Memoria por conversación (24/10/2026)

Prueba con `InMemorySaver` y Gemini 3.1 Flash-Lite, temperatura 1.0, máximo 1800 tokens, k=3 y filtro LMU. Se cargó el intercambio real de `outputs/agent_style.json` en una conversación temporal para evitar volver a generar el primer turno. Después se ejecutaron dos seguimientos con recuperación y generación nuevas: dos embeddings de consulta y dos llamadas al LLM, sin regenerar embeddings del corpus. Informe privado: `outputs/memory_evaluation.json`; respuestas completas en la sección 5 del notebook.

| Turno | Qué dijo el piloto ficticio | Resultado sobre memoria | Tokens entrada / salida |
| --- | --- | --- | --- |
| D04 | Todavía no ha cambiado nada; pregunta qué observar al probar la primera propuesta | Identifica la propuesta de barra estabilizadora trasera y habla de la prueba en futuro; no afirma que ya se haya aplicado. | 2896 / 348 |
| Seguimiento aplicado | Ha reducido la rigidez de la barra trasera y relata menos sobreviraje, todavía presente | Recuerda el cambio y la mejora parcial relatada; propone otra prueba de suspensión. | 3191 / 369 |

La continuidad está demostrada en esos dos mensajes, pero la fidelidad técnica sigue siendo parcial. En D04 añade pérdida de agilidad o subviraje a la entrada; en el siguiente turno añade tocar fondo y comportamientos en baches que no aparecen en la ficha `LMU_USH_24` citada. «Valida la dirección de trabajo» atribuye demasiada fuerza causal a un único efecto relatado por el piloto. Las citas existentes no bastan para validar esas afirmaciones. No presentar estas salidas como prueba de corrección física ni como una mejora medida.

Veintiuna pruebas locales sin API cubren corpus, recuperación, presentación y memoria. Las nuevas pruebas comprueban historial con roles, preparación del seguimiento antes de buscar, separación de conversaciones, confirmación al cambiar de simulador/coche, no heredar el coche entre simuladores, completar un coche desconocido, cancelación, fallo de API sin respuesta antigua ni duplicación del piloto, ausencia de documentos y rechazo de citas de turnos anteriores no recuperadas ahora. Las respuestas de los dobles locales no son respuestas reales de Gemini.

El contexto de coche y simulador se cambia mediante campos explícitos. Si el piloto solo lo menciona en el texto, el prompt pide actualizar y confirmar esos campos; esa detección depende del LLM. El historial guarda declaraciones originales, no un registro estructurado y validado de ajustes. La memoria es temporal, sin persistencia tras reiniciar. En estas pasadas solo se evaluó LMU; los otros casos se documentan a continuación. La comparación justa sin RAG con el mismo historial sigue pendiente.

## Cinco casos y chat (24/10/2026)

Informe agregado privado: `outputs/evaluation_cases.json`. Respuestas completas y preguntas en las secciones 4–6 del notebook, con referencias y procedencia. D01 se reutiliza del ejemplo de voz y D04 del seguimiento de memoria; D02 y D03 usan las búsquedas reales guardadas del 23/10 sobre el mismo corpus y generaciones nuevas. D05 realizó una búsqueda nueva. Las revisiones de D05 reutilizaron sus mismos fragmentos y conservaron las salidas anteriores en `outputs/evaluation_cases_before_*.json`.

| Caso | Resultado revisado | Fidelidad 0–2 | Contexto 0–2 | Memoria |
| --- | --- | --- | --- | --- |
| D01 · LMU | Propuesta de barra trasera respaldada; explicaciones y prioridad requieren más revisión. | 1 | 2 | No aplica a este caso aislado |
| D02 · iRacing | Reparto hacia atrás, criterio de bloqueo y presión general aparecen en las fichas citadas. Añade explicaciones no desarrolladas y pide datos de coche que el corpus no permite verificar por modelo. | 1 | 1 | No aplica |
| D03 · ACC | Wheel rate, fast bump y fast rebound coinciden con la ficha y se declara la antigüedad V1. La explicación de rigidez/absorción no está desarrollada en esa celda. | 1 | 2 | No aplica |
| D04 · seguimiento LMU | Recuerda la propuesta y que todavía no se aplicó. Añade efectos en entrada de curva que no respalda la ficha. | 1 | 2 | 2: distingue propuesta pendiente |
| D05 · falta de cifra exacta | Reconoce la ausencia de objetivo para modelo/versión, no inventa un número y limita el procedimiento a las fichas térmicas coherentes 10/11. | 2 | 2 | No aplica |

Las puntuaciones son revisiones manuales orientativas para estas preguntas, no medidas de corrección física ni un resultado global comparable. Todos los ID citados existen entre los fragmentos admitidos, pero varias frases siguen teniendo respaldo parcial. Se usaron distintas revisiones de prompt; no se agregan las puntuaciones ni se afirma una mejora frente al modelo base. La comparación posterior necesita condiciones equivalentes y una configuración documentada.

### Conflicto de presión y corrección aplicada

`LMU_USH_08` indica aumentar presión en su lista y disminuirla en la explicación para el centro del neumático más caliente. D05 inicial y una revisión de prompt eligieron una dirección sin señalarlo. Se conserva el original y se registra el conflicto en `prompts/source_quality.json`; la recuperación queda trazada en `documentos_recuperados` y la exclusión en `fuentes_excluidas`. La ficha se excluye de las recomendaciones, sin modificar corpus ni embeddings. La última generación D05 utiliza solo 10/11 y deja de aconsejar una dirección para ese centro caliente contradictorio. El registro es una revisión humana de una ficha conocida, no un detector general automático de conflictos.

Durante D05 también aparecieron citas agrupadas. Se corrigieron la validación de todos sus ID y su ocultación en `respuesta_piloto`, para que la futura web mantenga una respuesta limpia sin perder las evidencias internas.

### Uso y reproducibilidad

Esta fase hizo cinco generaciones para tres casos nuevos: D02 una, D03 una y D05 tres; las dos repeticiones se justificaron por el conflicto. Solo hubo un embedding de consulta nuevo. Tokens del LLM: 11709 de entrada y 1542 de salida. No se conocen cargos efectivos de la cuenta y no se ha cambiado su facturación. D01/D04 y las búsquedas previas no se repitieron.

`scripts/evaluate_cases.py` sin argumentos muestra ayuda sin API; `--run` completa pendientes y reutiliza resultados guardados. `--run --case D05 --repeat` repite explícitamente ese caso guardando una copia previa y reutilizando la recuperación. Cada respuesta conserva fecha, modelo, huella de prompt, documentos y uso. El arranque del notebook se comprobó en un kernel real con entrada `/salir` y las llamadas a generación/embeddings bloqueadas por la prueba: no se ejecutaron las demostraciones ni se consumió API.

Hay 31 pruebas locales, incluyendo el chat, cambios confirmados/cancelados, nueva conversación, errores, fuentes excluidas y citas agrupadas. Los dobles locales se usan solo para comprobar funcionamiento; las respuestas del notebook identificadas como reales proceden de los informes de Gemini. Quedan pendientes correcciones de fidelidad, web y presentación.

## Cinco salidas nativas del notebook (26/10/2026)

Se sustituyeron transcripciones en Markdown por cinco celdas de código realmente ejecutadas con Gemini 3.1 Flash-Lite. Se guardan los mensajes `display_data` recibidos de Jupyter, con sus contadores de ejecución reales (8–12); no se simularon resultados ni se trasladaron respuestas antiguas como si fueran ejecuciones nuevas. El setup y el chat también se ejecutaron; se envió `/salir` al prompt interactivo para continuar.

Una primera clasificación falló con `GoogleAPIError`, sin respuesta ni embedding; se conserva en `outputs/notebook_live_intento_fallido_1_2026-10-26.json`. La pasada completa posterior terminó los cinco ejemplos: 10 llamadas al modelo, 5 embeddings de consulta, 0 embeddings del corpus, 16.327 tokens de entrada y 1.153 de salida comunicados. Total: 11 llamadas incluyendo el intento fallido, cuyo consumo y facturación no se conocen. Informe: `outputs/notebook_live_2026-10-26.json`.

Los dos primeros ejemplos conservaron el contexto LMU/Ferrari y distinguieron la propuesta aún no aplicada; los siguientes usaron iRacing, ACC y LMU en sesiones nuevas. Todos los ID citados pertenecen a los fragmentos admitidos, y el último evitó una cifra exacta no documentada. Persisten límites técnicos: explicación del rake no verificada en 1/2; efecto en entrada añadido en 2; explicaciones y cita de reversión con respaldo parcial en 3; dos variables a la vez y mecanismos añadidos en 4; afirmación demasiado general de que una cifra «no existe» en 5, cuando solo se acredita que el corpus no la aporta. No son resultados de pista ni una validación completa del consejo.

Se dividieron literales largos para mejorar la lectura tras ejecutar y se verificó igualdad de AST; no se repitieron llamadas por ese cambio de formato. El núcleo y los prompts no cambiaron. Las respuestas históricas y tablas se mantienen en los informes, fuera del notebook simplificado.

## Primera web local (26/10/2026)

Se mantiene el chat del notebook. La web local reutiliza `crear_grafo` y Chroma existentes, pero solo muestra `respuesta_piloto`. 44 pruebas locales superadas: se añade apertura del índice sin embeddings y sin reparación automática, junto a 7 casos AppTest de recursos reales por sesión sin API, limpieza de fuentes, no repetir llamadas al rerenderizar, cambio confirmado, reinicio que elimina checkpoints, fallos de generación/clasificación y errores de configuración sin exposición de detalles. Las 7 pruebas de web se repitieron tras bloquear los controles durante el procesamiento. Las respuestas controladas de AppTest son pruebas funcionales; no se presentan como generaciones de Gemini.

La primera prueba de aislamiento con la caché de recursos por sesión detectó que AppTest emplea un identificador interno fijo para todos sus ejecutores. Se simplificó la aplicación para conservar el agente directamente en session_state; las pruebas verifican dos grafos y checkpointers distintos y reutilización en reruns. El código final no depende de esa caché.

Prueba real en navegador: un primer envío no se completó y mostró el mensaje de error genérico; no se capturó la causa interna. Se repitió manualmente y completó la consulta LMU/Ferrari GT3 con una primera propuesta. El seguimiento «todavía no he cambiado nada» conservó el contexto y se refirió a esa propuesta como futura. No se mostraron IDs ni enlaces documentales. Capturas y texto accesible en `outputs/web_smoke_2026-10-26.*`. No se midieron tokens ni facturación de esos tres envíos; no se infiere un coste. Las respuestas siguen incluyendo explicaciones técnicas que requieren revisión; la prueba verifica integración y memoria, no corrección física.

Se ha revisado la página en el navegador integrado, incluido el diseño adaptable con barra lateral plegable. La web queda accesible solo en este equipo; no se ha publicado ni desplegado.
