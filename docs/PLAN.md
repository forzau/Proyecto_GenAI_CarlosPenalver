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
| 5 | Evaluar y corregir; comenzar Streamlit si el núcleo funciona | Al menos un caso por simulador, 5 respuestas reales, seguimiento y comparación con modelo base |
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
- [ ] Elegir el modelo de generación y probar el LLM al implementar el agente.
- [x] Indexar 75 fichas con Gemini Embedding 2 en Chroma; verificar persistencia y tres consultas filtradas.
- [ ] Implementar LangGraph con recuperación en cada consulta.
- [ ] Integrar y justificar el prompt final en README.
- [ ] Implementar memoria y demostrar un seguimiento.
- [ ] Crear chat de texto en notebook y documentar al menos 5 preguntas/respuestas reales.
- [ ] Comparar Gemini sin RAG con el agente sobre los mismos casos.
- [ ] Completar README con instrucciones probadas y limitaciones reales.
- [ ] Preparar presentación y demo de 5–10 minutos.
- [ ] Bonus: interfaz Streamlit.
- [ ] Bonus: URL pública, secretos fuera de Git y memoria aislada por sesión.

## Guion previsto de la presentación

1. Problema y usuario: 1 minuto.
2. Corpus, prompt y arquitectura: 2 minutos.
3. Demo: consulta, fuentes, seguimiento y caso sin evidencia: 3 minutos.
4. Comparación con Gemini sin RAG, límites y próximos pasos: 1–2 minutos.

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
