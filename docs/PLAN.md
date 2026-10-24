# Plan de trabajo y entrega

## Decisiones y estado

Setup iniciado el 22/10/2026. El alumno indica una semana de plazo; confirmar el día y la hora exactos. Mantener Gemini como único proveedor. La web está prevista como bonus después del MVP.

Dominio confirmado: ingeniero de boxes para simracing, con diagnóstico general e iRacing, ACC y Le Mans Ultimate. Corpus seleccionado y preparado: 75 fichas de tres fuentes; coches y versiones no especificados. Demo documental, sin pruebas en pista. Ver DOMINIO.md.

El PDF original está en la raíz local de Proyecto. Sus pasos 2 y 3 tienen los títulos intercambiados respecto al contenido: este plan agrupa las tareas por lo que realmente requieren.

## Siete días

| Día | Trabajo | Evidencia para darlo por terminado |
| --- | --- | --- |
| 1 | Seleccionar corpus y casos documentales, empezando por LMU y ampliando a los otros dos simuladores | Fuentes, versiones y cobertura documentadas; no requiere recuerdos de incidencias del alumno |
| 2 | Cargar, segmentar e indexar documentos | Chroma persistente; metadatos de simulador/coche/versión y filtros revisados antes del agente |
| 3 | Prompt y grafo LangGraph con Gemini | Pregunta → recuperación → generación; respuesta sustentada en fragmentos |
| 4 | Memoria y notebook interactivo | Seguimiento de cambios confirmados, revisión al cambiar de coche/simulador y aislamiento entre conversaciones |
| 5 | Evaluar y corregir; comenzar Streamlit si el núcleo funciona | Al menos un caso por simulador, 5 respuestas reales y seguimiento |
| 6 | Completar web y preparar presentación | Interfaz local funcional, README actualizado y guion de demo |
| 7 | Ensayar y revisar entrega; desplegar bonus si es viable | Ejecución desde entorno limpio y demo de 5–10 minutos sin pasos improvisados |

## Lista de entrega

- [x] Revisar enunciado y notebooks de clase.
- [x] Preparar estructura, variables de entorno y protección de archivos locales.
- [x] Preparar notebook de trabajo, borrador del prompt y plan de evaluación.
- [x] Confirmar dominio, usuario objetivo y alcance de diagnóstico para iRacing, ACC y LMU.
- [x] Acotar demo a consultas documentales de las guías seleccionadas; no exigir acceso al simulador.
- [x] Localizar fuentes oficiales y capturar cinco originales con inventario de procedencia (23/10/2026).
- [x] Seleccionar las tres fuentes del MVP y registrar procedencia, fecha, límites y huellas.
- [x] Capturar 25 hojas de LMU y transcribir visualmente 20 celdas de iRacing y 30 de ACC; preparar JSONL y carga en notebook.
- [x] Instalar y comprobar el entorno independiente.
- [x] Elegir y utilizar Gemini Embedding 2, como en clase.
- [x] Elegir Gemini 3.1 Flash-Lite y probar el LLM al implementar el agente.
- [x] Indexar 75 fichas con Gemini Embedding 2 en Chroma; verificar persistencia y tres consultas filtradas.
- [x] Implementar LangGraph con recuperación en cada consulta de un turno.
- [x] Integrar y justificar el prompt del flujo básico en README; revisar al añadir memoria.
- [x] Implementar memoria temporal por conversación y demostrar dos seguimientos.
- [x] Crear chat de texto en notebook y documentar cinco preguntas/respuestas reales, con los tres simuladores y seguimiento.
- [ ] Completar README con instrucciones probadas y limitaciones reales.
- [ ] Preparar presentación y demo de 5–10 minutos.
- [ ] Bonus: interfaz Streamlit.
- [ ] Bonus: URL pública, secretos fuera de Git y memoria aislada por sesión.

## Guion previsto de la presentación

1. Problema y usuario: 1 minuto.
2. Corpus, prompt y arquitectura: 2 minutos.
3. Demo: consulta, fuentes, seguimiento y caso sin evidencia: 3 minutos.
4. Revisión documental, límites y próximos pasos: 1–2 minutos.

## Registro de decisiones

- Separar el proyecto del entorno de clase para reproducir la instalación.
- Mantener los documentos originales y el índice fuera de Git; versionar su inventario y las instrucciones de reproducción.
- Priorizar notebook y núcleo antes de la interfaz.
- Usar escenarios de sesión ficticios para evaluar razonamiento y memoria; no presentarlos como pruebas realizadas en pista.
- Un solo agente para los tres simuladores, con filtros documentales y comprobaciones de aplicabilidad.
- Cubrir diagnóstico general y ajustes respaldados; no prometer compatibilidad con todos los coches y versiones.
- No añadir telemetría en directo, voz, edición automática de setups ni agentes múltiples durante esta semana.

## Verificacion del setup (22/10/2026)

- Entorno independiente creado con Python 3.12.3; dependencias instaladas y `pip check` sin conflictos.
- Las dos celdas de preparacion se han ejecutado desde la raiz y desde `notebooks/`, con importaciones correctas y sin llamadas a Gemini.
- Estructura y sintaxis del notebook, enlaces locales y exclusiones de Git comprobados.
- Revisados los archivos preparados para Git: no incluyen entorno, corpus, indice ni claves reconocibles.
- No se ha validado aun RAG, memoria, calidad de respuestas ni la web: su implementacion queda pendiente.

## Corpus preparado (23/10/2026)

- Selección cerrada por el alumno: Ultimate Setup Hub para LMU, chuleta Chris Haye del artículo SimRacingCockpit para iRacing y PDF Driver61 V1 para ACC.
- 38 páginas del árbol público visitadas y 25 hojas capturadas; 50 fichas adicionales transcritas visualmente de las dos láminas. Total: 75 fichas con fuente, localizador y simulador.
- Inventario activo en `docs/corpus_mvp.json`; constructor local y carga de documentos en el notebook. Las seis capturas previas quedan como reserva en `docs/corpus.json`.
- Versión de juego y coche desconocidos; antigüedad y límites registrados. No hace falta probar reglajes para esta entrega: se evaluará respaldo documental, recuperación, citas y memoria.
- Fase siguiente completada: índice Chroma y tres búsquedas comprobadas; queda implementar el agente con un LLM de Gemini.
- Tarea opcional del alumno: proponer una pregunta por simulador y un seguimiento. No necesita conocer la respuesta ni volver a jugar.

## Índice y recuperación comprobados (23/10/2026)

- Revisados `rag_profesor.ipynb` y `clase3.ipynb`. Mismo flujo: cliente de embeddings, `Chroma.from_documents`, persistencia y búsqueda por similitud.
- Gemini Embedding 2, 3072 dimensiones, coseno, una ficha completa por fragmento, solapamiento 0. Adaptación para retirar `task_type` y aplicar los prefijos de búsqueda de Embedding 2.
- Colecciones identificadas por corpus, modelo y formato: reabrir no duplica fichas ni recalcula el corpus. Las colecciones anteriores se conservan si cambia la configuración.
- Notebook ejecutado de principio a fin: 75 fichas guardadas; reapertura comprobada. Tres consultas en español con ficha esperada en top 3 y sin mezcla de simuladores: LMU posición 1, iRacing y ACC posición 2.
- Pruebas automáticas locales sin API para formato de petición, persistencia, reutilización, separación de corpus, filtros e inputs inválidos.
- Uso real limitado a la indexación del corpus y tres consultas; la prueba inicial con la credencial heredada fue rechazada antes de copiar la clave autorizada de clase. No se generaron respuestas de chat. No se conoce facturación efectiva de la cuenta; no se activó ni modificó.
- Siguiente trabajo: Gemini LLM, prompt y grafo LangGraph. No ampliar el corpus ni repetir consultas de API por rutina.

## Presentación del notebook simplificada (23/10/2026)

- Retirados asserts, comprobaciones de entorno y pruebas de persistencia del notebook. Celdas directas: configuración, corpus, embeddings, Chroma y un ejemplo de búsqueda.
- La evaluación real de tres consultas queda en `scripts/evaluate_retrieval.py`; las pruebas automáticas permanecen en `tests/`. Los resultados anteriores se conservan en EVALUACION.md y en el informe local.
- Sin nuevas llamadas a Gemini por este cambio.

## Cierre y continuación en otro equipo (23/10/2026)

- Guía de estado, traslado e instalación en [CONTINUAR.md](CONTINUAR.md). Rama: `setup-inicial`.
- Paquete local fuera de Git: `outputs/continuar_otro_equipo_2026-10-23.zip`, con corpus activo, copia consistente de Chroma, resultados y versiones del entorno; sin claves ni `.venv`. Restauración local comprobada sin consumir API.
- Próxima fase: elegir Gemini LLM e implementar el agente LangGraph con recuperación y fuentes; después, memoria.

## Entorno recreado en este equipo (24/10/2026)

- Instalado Python 3.12.10 para el usuario y recreado `.venv` con las versiones de `outputs/requirements-session.txt`. El entorno anterior se conserva temporalmente en `outputs/venv_anterior_2026-10-24/`, fuera de Git.
- `pip check` sin conflictos; importaciones de kernel, LangGraph, Gemini y recuperación correctas. Las cinco pruebas locales han pasado sin llamadas a Gemini.
- Kernel registrado: `Python 3.12 (Proyecto Simracing)`.
- OneDrive bloqueaba la lectura de cachés antiguas; las tres cachés afectadas se han renombrado con sufijo `.anterior`. También bloquea la lectura de `.env`, todavía solo en la nube: se ha solicitado mantenerlo descargado, sin leer ni mostrar la clave. Las comprobaciones se ejecutaron desde la carpeta superior, con `Proyecto` en `PYTHONPATH`, para evitar esa lectura automática de Chroma. Antes de ejecutar el notebook, comprobar que `.env` está disponible localmente.
- Sin cambios en corpus ni índice y sin regenerar embeddings. La siguiente fase sigue siendo implementar el agente.

## Incidencia de OneDrive (24/10/2026)

- `.env`, corpus, Chroma y ZIP de traslado siguen siendo archivos solo en la nube. El ZIP devuelve `0x8007017C` («La operación de nube no es válida»); su existencia y tamaño en el Explorador no prueban que se pueda leer.
- Realizado un cierre y reinicio normal de OneDrive y, al persistir el fallo, el restablecimiento oficial con `/reset`. La sincronización se está reconstruyendo; todavía no se ha verificado la recuperación de los archivos.
- `SyncDiagnostics.log` registra 509.757 archivos y 69.809 carpetas y aborta una verificación por exceso de elementos. Es un indicio de sobrecarga, no una causa confirmada. Microsoft recomienda un máximo estándar de 300.000 elementos fuera de su vista previa ampliada.
- Copia local de este plan previa al restablecimiento en `%LOCALAPPDATA%/Codex/Recovery/IA_Generativa_2026-10-24/PLAN.md`, fuera de OneDrive.
- Alternativa preparada: descargar el ZIP de traslado y `.env` desde OneDrive web con la cuenta UMH; el navegador solicita iniciar sesión. No se ha recuperado ninguna clave ni regenerado embeddings. Para continuar, conviene restaurar una copia de trabajo fuera de OneDrive y recrear allí el entorno, conservando el original.

## Recuperación local completada (24/10/2026)

- Copia activa: `C:\Users\forza\Projects\Proyecto_GenAI_CarlosPenalver`, clonada desde `setup-inicial`. Conserva las anotaciones de este plan y la carpeta anterior de OneDrive.
- El alumno descargó el ZIP y la configuración privada desde OneDrive web. Paquete íntegro y todas las huellas del inventario comprobadas; restaurados corpus, SQLite de Chroma, resultados y versiones. Configuración disponible localmente, sin mostrar la clave.
- Entorno nuevo con Python 3.12.10 y las versiones de `outputs/requirements-session.txt`; `pip check` sin conflictos y cinco pruebas locales superadas desde la raíz del proyecto.
- Chroma abre las 75 fichas. Una consulta con un vector ya guardado recupera su propia ficha para cada simulador, con filtro y 3072 dimensiones. Son comprobaciones técnicas locales; no una nueva evaluación semántica. Sin llamadas a Gemini ni embeddings nuevos.
- Kernel `Python 3.12 (Proyecto Simracing)` actualizado para apuntar al entorno de esta copia local. El notebook conserva su flujo sencillo, sin nuevas celdas de comprobación.
- La recuperación permite continuar el proyecto independientemente de OneDrive. No se ha demostrado que la sincronización general de OneDrive haya quedado reparada. Siguiente fase: Gemini LLM y LangGraph con fuentes, después memoria.

## Flujo básico implementado (24/10/2026)

- Modelo elegido por la disponibilidad indicada por el alumno: `gemini-3.1-flash-lite`, configurable en `.env`. Temperatura 1.0, máximo de 1800 tokens de salida, 45 s de espera y un intento. Sin cambio automático de modelo ni facturación configurada por esta sesión.
- Revisado `clase_LangGraph.ipynb`. `agent.py` sigue su patrón: estado `TypedDict`, nodos `recuperar` y `responder`, enlaces y compilación. Reutiliza `search` de `retrieval.py` y el prompt especializado.
- Recuperación en cada consulta, filtro por simulador y metadatos completos enviados al LLM. Salida con respuesta, fuentes citadas, documentos y uso de tokens. Se bloquean los ID no recuperados; la fidelidad del texto se revisa por separado.
- Diez pruebas locales sin API: corpus, persistencia, filtros, recuperación por llamada, no arrastrar fuentes entre invocaciones independientes, resultados vacíos, entradas inválidas, citas inexistentes y error del LLM. No prueban memoria: aún no existe.
- Notebook ejecutado con kernel real desde la copia local. Una consulta LMU, repetida una vez tras detectar una explicación aerodinámica no respaldada. Prompt reforzado para limitar mecanismos a las fuentes y conservar sus supuestos. Dos embeddings de consulta y dos generaciones, sin reindexar las 75 fichas.
- Informes privados en `outputs/agent_smoke_initial.json` y `outputs/agent_smoke.json`; segunda respuesta guardada en el notebook. Tokens del LLM: primera pasada 1859 de entrada y 488 de salida; segunda 2009 y 450. No se conoce la facturación efectiva; no se ha activado ni modificado.
- Las salidas son escenarios documentales ficticios. Un caso y su revisión no demuestran corrección general ni mejora en pista. Pendientes memoria, cinco casos distintos, comparación sin RAG y web.

## Voz del ingeniero revisada (24/10/2026)

- Preferencia del alumno: voz de ingeniero de coche con propiedad, sin repetir «según la guía». Se ha eliminado del prompt la obligación de atribución verbal repetitiva; se mantienen citas, límites de aplicabilidad, hipótesis y respaldo documental.
- Respuestas más directas, una prueba principal y menos estructura de informe. La incertidumbre se expresa en el punto donde afecta a la decisión. Los criterios de reversión deben centrarse en el síntoma y en las mismas condiciones.
- Una generación real de Gemini 3.1 Flash-Lite sobre las tres fichas LMU ya recuperadas; cero embeddings nuevos. Informe privado: `outputs/agent_style.json`. Uso del LLM: 2394 tokens de entrada y 325 de salida.
- Ejemplo real guardado en Markdown en la sección 4 del notebook. Se han limpiado las salidas antiguas de las celdas de código para no presentarlas como ejecuciones del nuevo prompt. Las pasadas anteriores se conservan en `outputs/agent_smoke*.json` y la copia previa del notebook en `outputs/proyecto_antes_estilo.ipynb`.
- La prueba mejora el tono en este caso; no demuestra más conocimiento ni fidelidad global. Las propuestas de barra estabilizadora y diferencial figuran en la ficha citada. La elección del ajuste principal varía respecto a la pasada anterior: la consistencia de priorización queda para la evaluación. Siguiente desarrollo: memoria.

## Citas por interfaz (24/10/2026)

- El alumno quiere respuestas sin fuentes visibles en la futura web. El notebook conserva las citas y los localizadores para comprobar el respaldo durante el desarrollo.
- `agent.py` conserva `respuesta`, `fuentes` y `documentos`, y añade `respuesta_piloto`: texto sin marcadores, enlaces documentales ni bloque bibliográfico final. La eliminación de referencias se aplica después de comprobar los ID citados, sin otra generación.
- Once pruebas locales superadas. Se comprueba que la presentación limpia conserva el texto técnico y que la respuesta original y sus evidencias siguen disponibles. Ninguna llamada a Gemini ni a embeddings por este cambio. La web todavía está pendiente de implementación.

## Memoria temporal implementada (24/10/2026)

- `InMemorySaver` y `thread_id`, siguiendo `clase_agentes.ipynb`. El grafo añade un nodo `preparar` antes de recuperar y mantiene contexto e historial con roles. El notebook crea una conversación y ofrece dos seguimientos con la misma configuración; otro identificador inicia una sesión independiente.
- Las búsquedas de seguimiento incluyen antecedentes del piloto y la última propuesta. Una recomendación no se registra como aplicada por el código: se conservan las declaraciones originales y el prompt interpreta las confirmaciones. No se añade otra llamada LLM para resumir o reescribir la consulta.
- Cambiar de simulador o de coche conocido pide confirmación sin API. Al confirmar, se inicia el nuevo contexto sin el historial activo anterior; no se hereda el coche al cambiar de simulador. Completar un coche desconocido conserva el historial. Los cambios de contexto se indican en campos explícitos; los mencionados solo en texto necesitan aclaración del modelo y actualización de esos campos.
- Veintiuna pruebas locales sin API: se añaden límites de memoria, aislamiento, confirmación, cancelación, error sin respuesta antigua, ausencia de documentos y rechazo de citas que solo existían en turnos anteriores.
- Prueba real: se cargó el intercambio LMU real guardado en `outputs/agent_style.json` y se ejecutaron dos seguimientos nuevos. Primero, ajuste todavía no aplicado; después, barra trasera aplicada y efecto parcial ficticio relatado. Dos embeddings de consulta y dos generaciones, sin reindexar el corpus. Informe privado: `outputs/memory_evaluation.json`; respuestas reales guardadas en Markdown en la sección 5 del notebook.
- Tokens del LLM: primer seguimiento 2896 de entrada y 348 de salida; segundo 3191 y 369. La revisión muestra continuidad de conversación, pero todavía hay extrapolaciones físicas que no respalda la ficha citada; ver EVALUACION.md. No se ha demostrado fidelidad general ni mejora en pista.
- La memoria vive en RAM y se pierde al reiniciar; no se añade base de datos ni servicio. Pendientes chat interactivo, completar casos de iRacing/ACC y falta de evidencia, comparación sin RAG y web. No repetir las llamadas reales por rutina.

## Chat y cinco casos documentados (24/10/2026)

- Chat funcional en la sección 6 del notebook: `/salir`, `/nuevo`, `/simulador`, `/coche`, `/confirmar` y `/cancelar`. Cada chat empieza un identificador propio. Los cambios de contexto se confirman antes de procesar la pregunta pendiente. El chat puede continuar tras errores de API y no muestra el detalle interno del proveedor.
- Las consultas de demostración de las secciones 4 y 5 se han convertido en ejemplos de código opcionales para que ejecutar el notebook no gaste tres llamadas antes de abrir el chat. Los ejemplos reales permanecen guardados en Markdown.
- 31 pruebas locales sin API, incluyendo el controlador real del chat leído del notebook, aislamiento, cancelación, confirmación, errores y presentación sin fuentes. Arranque comprobado en un kernel real: configuración, índice, entrada por stdin y `/salir`; cero llamadas API en esa comprobación, con métodos de red bloqueados por la prueba.
- Cinco preguntas reales documentadas: D01 LMU, D02 iRacing, D03 ACC, D04 seguimiento sin cambio aplicado y D05 presión exacta no respaldada. Se conservan además el seguimiento aplicado y los intentos de revisión. No se cuentan generaciones repetidas como preguntas distintas.
- Evaluación privada en `outputs/evaluation_cases.json` y `scripts/evaluate_cases.py`. Se reutilizaron D01/D04 y las búsquedas anteriores de D02/D03. Esta fase consumió cinco generaciones y un embedding de consulta: D02/D03 una vez cada uno, D05 tres pasadas para revisar su respuesta y una contradicción documental. Tokens del LLM: 11709 de entrada y 1542 de salida. No se conoce facturación efectiva ni se ha activado o modificado.
- `LMU_USH_08` contiene una contradicción entre lista y explicación. Se conserva en el corpus y se marca en `prompts/source_quality.json` para excluirla de la evidencia de recomendaciones, sin reindexar. El resultado registra candidatos, fragmentos admitidos y exclusiones. Se corrigió también la validación y ocultación de citas agrupadas.
- D05 final reconoce la falta de una cifra exacta para coche/versión y se apoya solo en las fichas coherentes 10/11. La evaluación de D01–D04 sigue siendo parcial por extrapolaciones anotadas; la muestra contiene revisiones de prompt diferentes y no demuestra una mejora global frente a Gemini sin RAG.
- Siguiente fase: revisión del notebook por el alumno y mejoras de fidelidad. Después, web y presentación. Cambios de esta sesión locales; todavía no se han publicado en GitHub.

Decisión del alumno (24/10/2026): se descarta la comparación sin RAG y se retira del notebook. Era una evaluación adicional propuesta durante la planificación, no una exigencia del enunciado. El alumno revisará ahora el notebook para proponer mejoras. Esta decisión sustituye las referencias históricas anteriores a la comparación como pendiente.

## Cierre del 24/10/2026

Sesión terminada por el alumno. Siguiente sesión: propuestas de mejora del notebook y web en Streamlit. Se versionan el agente, memoria, chat, cinco ejemplos documentados y las pruebas locales (31 superadas, sin API); las mejoras de fidelidad siguen pendientes. Paquete de traslado privado actualizado al 24/10/2026 y guía en CONTINUAR.md. La comparación sin RAG queda fuera del alcance.
