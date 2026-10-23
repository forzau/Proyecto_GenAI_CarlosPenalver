# Fuentes y corpus

## Dónde buscar y qué priorizar

Revisión del 23/10/2026. Prioridad: documentación del desarrollador, manuales del coche elegido y cambios de versión. Las guías originales de especialistas son complementarias y deben contrastarse; foros y vídeos sirven para localizar problemas o explicaciones, no para convertir opiniones aisladas en reglas del agente.

### iRacing

| ID | Fuente | Qué aprovechar | Estado y límites |
| --- | --- | --- | --- |
| IR01 | [Catálogo oficial de manuales de coches](https://www.iracing.com/resources/user-manuals/) | Manual del coche elegido: ajustes disponibles, funcionamiento y restricciones | Falta elegir coche; el catálogo no cuenta como documento del corpus |
| IR02 | [Guía de iniciación alojada por soporte de iRacing](https://support.iracing.com/support/solutions/articles/31000168572) | Método para describir síntomas y enlaces a documentación de reglajes | Seleccionar secciones; excluir gráficos y periféricos |
| IR03 | [Shock Tuning User Guide](https://s100.iracing.com/wp-content/uploads/2021/08/Shock-Tuning-User-Guide.pdf) | Amortiguadores, terminología y diagramas | Copia PDF local: 20 páginas brutas; revisión de contenido y aplicabilidad pendiente |
| IR04 | [iRacing Car Setup Guide](https://ir-core-sites.iracing.com/members/pdfs/iRacing_Car_Setup_Guide_20100910.pdf) | Referencia histórica y método de ajuste | Enlace verificado; documento de 2010, no tomar sus valores como actuales |

### Assetto Corsa Competizione

| ID | Fuente | Qué aprovechar | Estado y límites |
| --- | --- | --- | --- |
| ACC01 | [Notas oficiales de física v1.9](https://assettocorsa.gg/wp-content/uploads/ACCv19-physics_notes.pdf) | Cambios documentados de neumáticos y física de esa versión | Copia PDF local: 8 páginas brutas; referencia histórica, sin validación para otra versión |
| ACC02 | [Soporte de 505 Games: changelog v1.10.4 para PC](https://support.505games.com/support/solutions/articles/150000217831-assetto-corsa-competizione-changelog-v1-10-4-2025-dec-22-pc-) | Complemento de versión; seguir la cadena de cambios que afecten al caso | No es un manual de setup ni demuestra por sí solo que todos los valores de v1.9 sigan vigentes |
| ACC03 | [Coach Dave: guía de subviraje y sobreviraje](https://coachdaveacademy.com/tutorials/how-to-fix-oversteer-and-understeer-in-acc/) | Explicación original de un especialista, candidata para conceptos y relaciones entre ajustes | Complementaria, publicada en 2020; contrastar antes de incorporarla; no requiere comprar setups |

Para ACC falta una guía de reglajes aplicable a la versión y coche de demo. Las notas v1.9 y un changelog de contenido no cierran esa laguna. Priorizar documentos técnicos del desarrollador y explicaciones del propio equipo de físicas; si se usa un vídeo, registrar autor, fecha y marcas de tiempo y revisar su transcripción. No usar una transcripción generada sin verificar.

### Le Mans Ultimate

| ID | Fuente | Qué aprovechar | Estado y límites |
| --- | --- | --- | --- |
| LMU01 | [Guía oficial: sección On Track](https://guide.lemansultimate.com/hc/en-gb/sections/13152333627151-On-Track) | Navegación hacia artículos concretos de controles y comportamiento | No indexar el catálogo como contenido sustancial |
| LMU02 | [LMP3 Quick Setup Guide](https://lemansultimate.com/lmp3-quick-setup-guide/) | Ajustes de los LMP3 descritos por el desarrollador | Copia HTML local; depende de coches, capturas y versión; no extrapolar a GT3 o Hypercar |
| LMU03 | [Configuración del control de tracción](https://guide.lemansultimate.com/hc/en-gb/articles/13182869047311-How-do-I-configure-my-traction-control-in-Le-Mans-Ultimate) | Función de los controles y cómo localizarlos | Copia HTML local; limpiar navegación y revisar capturas |
| LMU04 | [ABS para LMGT3](https://guide.lemansultimate.com/hc/en-gb/articles/13211078435983-ABS-Anti-Lock-Braking-System-for-LMGT3-Cars) | Alcance por categoría y explicación de mapas | Copia HTML local; la tabla de mapas es una imagen: revisión y transcripción visual pendientes |
| LMU05 | [MFD y datos que muestra](https://guide.lemansultimate.com/hc/en-gb/articles/13202210967055-Understanding-the-MFD-Multi-Function-Display) | Qué información puede aportar el piloto al diagnóstico | Enlace localizado; no implica que el agente lea telemetría |

## Copias locales e inventario

Se han guardado cinco originales en `data/corpus/pendientes/`: IR03, ACC01, LMU02, LMU03 y LMU04. Hay dos PDF (28 páginas brutas en total) y tres artículos HTML. El [inventario de capturas](corpus.json) registra procedencia, autor, formato, ruta, tamaño, fecha, SHA-256 y límites conocidos. Las copias originales permanecen fuera de Git; el inventario se versiona.

**No están limpios, aprobados para responder ni indexados.** `pendientes/` no deberá entrar en la indexación hasta revisar cada fuente y su aplicabilidad. El volumen bruto no equivale a páginas útiles; tablas e imágenes pueden contener información que no aparece en la extracción de texto.

Objetivo: al menos tres documentos sustanciales y unas 20 páginas equivalentes útiles, con casos respaldados de los tres simuladores. La selección final tendrá que añadir el manual del coche de iRacing y completar ACC según los casos elegidos. No comprar contenido ni recopilar cientos de páginas para empezar.

## Tarea del alumno en paralelo

Completar [CASOS_PILOTO.md](CASOS_PILOTO.md) con un coche conocido y un problema por simulador. Si no dispone de un simulador, indicarlo; no inventar observaciones reales. Los casos guían la selección del corpus y se mantendrán separados de los documentos de conocimiento para no filtrar respuestas a la evaluación.

## Registro al incorporar cada documento

Anotar ID, título, autor, URL original o procedencia, fecha de consulta, fecha/versión del documento, versión de juego aplicable si se conoce, archivo local, idioma, extensión útil, permiso/licencia y limpieza realizada. Si no se puede redistribuir, indicar cómo obtenerlo en lugar de subirlo.

La fecha de consulta no demuestra que un documento sea aplicable a la versión actual del juego. Registrar por separado las versiones conocidas y las desconocidas. Las notas de actualización complementan los manuales; no asumir que una guía anterior sigue vigente sin contrastarla.

## Metadatos y recuperación previstos

Cada fragmento conservará ID de documento, título, URL, página o sección e ID de fragmento, además de:

- `simulator`: `iracing`, `acc`, `lmu` o `general`. El valor `general` requiere revisar su aplicabilidad; no se usa como comodín para documentos específicos.
- Coche o categoría cubierta y versión aplicable, cuando consten; lo desconocido se registra como desconocido.
- Fecha y versión del documento, y tema del fragmento cuando ayude a comprobar su alcance.

Filtrar por simulador antes de recuperar: documentos del simulador elegido más fundamentos generales revisados. Comprobar coche, versión y unidades antes de recomendar cifras o ajustes específicos. Si no hay fuente aplicable, reconocer la laguna. Al cambiar simulador o coche, volver a recuperar con el nuevo contexto.

Si cambia el modelo de embeddings o la segmentación, reconstruir el índice y registrar la configuración utilizada. Los documentos se guardarán en `data/corpus/` y el índice en `data/chroma/`, ambos excluidos de Git. El inventario debe permitir reproducir el corpus.

## Referencias locales de clase

| Notebook en ../Notebooks/ | Qué reutilizar como referencia |
| --- | --- |
| rag_profesor.ipynb y clase3.ipynb | Carga de PDF, chunking, Chroma y recuperación; usar Gemini Embeddings según el enunciado |
| clase_LangGraph.ipynb | Estado, nodos, aristas y flujo del grafo |
| clase_agentes.ipynb | Historial, mensajes y checkpointer de memoria |
| clase2.ipynb | Configuración de Gemini y composición de prompts |

Son referencias de aprendizaje. No copiar sus claves, sus bases vectoriales ni sus salidas a este proyecto.
