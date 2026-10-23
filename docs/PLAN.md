# Plan de trabajo y entrega

## Decisiones y estado

Setup iniciado el 22/10/2026. El alumno indica una semana de plazo; confirmar el día y la hora exactos. Mantener Gemini como único proveedor. La web está prevista como bonus después del MVP.

Dominio confirmado: ingeniero de boxes para simracing, con diagnóstico general e iRacing, ACC y Le Mans Ultimate. Falta seleccionar el corpus y concretar los coches y versiones de demo. Ver DOMINIO.md.

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
- [ ] Concretar coches, versiones y casos de demo según el corpus disponible.
- [x] Localizar fuentes oficiales y capturar cinco originales con inventario de procedencia (23/10/2026).
- [ ] Seleccionar corpus suficiente; registrar autor, origen, fecha y permisos.
- [ ] Limpiar texto, revisar tablas/imágenes y comprobar versión y cobertura de cada documento antes de indexar.
- [x] Instalar y comprobar el entorno independiente.
- [ ] Elegir modelos disponibles y probar una llamada controlada a Gemini.
- [ ] Indexar corpus con Gemini Embeddings en ChromaDB y verificar recuperación.
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

## Avance de fuentes (23/10/2026)

- Cinco copias originales locales e inventario en `docs/corpus.json`: dos PDF con 28 páginas brutas y tres HTML.
- Limpieza, revisión visual, aplicabilidad y suficiencia útil pendientes; todavía no existe un índice Chroma.
- Prioridad siguiente, ajustada al contexto del alumno: limpiar y revisar LMU primero, preparar preguntas documentales y después completar manuales de iRacing y documentación de ACC.
- El alumno solo ha jugado LMU, principalmente un Ferrari GT3 (modelo exacto pendiente), que recuerda como más estable para empezar. Recuerda dificultad con el sobreviraje; versión y fase desconocidas. El relato se usará para probar si el agente pide contexto sin inventar causas.
- Priorizar fuentes aplicables a LMGT3; mantener la guía LMP3 como complemento, sin extrapolar sus ajustes.
- Tarea paralela opcional del alumno: precisar el modelo del Ferrari GT3 si lo recuerda, sin necesidad de volver a jugar.
- Si falta evidencia suficiente para especialización, valorar con el alumno un experto en fundamentos generales de simracing; no cambiar de alcance automáticamente.

## Revisión de la guía aportada por el alumno (23/10/2026)

- Añadida IR04: guía de iRacing creada en 2010, 22 páginas; revisión inicial de método y terminología, con páginas 2, 3 y 22 comprobadas visualmente.
- Corpus actual: seis copias originales, tres PDF con 50 páginas brutas y tres HTML. Ninguna está indexada; IR04 no está aprobada íntegramente.
- La tabla final de IR04 no devuelve texto útil con pypdf y queda excluida de una primera indexación sin transcripción revisada.
- Ferrari GT3 registrado como experiencia del alumno; modelo exacto pendiente y estabilidad anotada como impresión personal.
