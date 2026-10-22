# Fuentes y corpus

## Candidatas para simracing

Enlaces consultados el 22/10/2026. Son candidatos, no documentos descargados, validados para una versión concreta ni indexados. Cubriremos iRacing, ACC y LMU con la profundidad que permita la evidencia; no mezclar sus parámetros.

| ID | Fuente | Uso previsto y límites | Estado |
| --- | --- | --- | --- |
| IR01 | [iRacing: manuales oficiales](https://www.iracing.com/resources/user-manuals/) | Elegir manuales de los coches de demo y comprobar versión y parámetros disponibles | Catálogo localizado; documentos por elegir |
| IR02 | [iRacing: guía de iniciación y setup](https://support.iracing.com/support/solutions/articles/31000168572) | Seleccionar secciones de comportamiento y método de prueba, excluyendo configuración gráfica y periféricos | Revisar secciones y enlaces a guías de setup |
| ACC01 | [ACC: notas oficiales de física v1.9](https://assettocorsa.gg/wp-content/uploads/ACCv19-physics_notes.pdf) | Referencia histórica identificada por versión; contrastar con cambios posteriores antes de recomendar valores | Pendiente de extracción y contraste; no asumir vigencia actual |
| LMU01 | [LMU: guía oficial](https://guide.lemansultimate.com/hc/en-gb) | Seleccionar artículos sobre vehículo, setup y condiciones; una portada no cuenta como documento sustancial | Artículos por elegir |
| LMU02 | [LMU: guía oficial de setup LMP3](https://lemansultimate.com/lmp3-quick-setup-guide/) | Posible caso específico LMP3; no extrapolar a GT3 o Hypercar ni a otra versión | Revisar aplicabilidad antes de incorporarla |
| GEN01 | Documento de fundamentos de dinámica y método de diagnóstico | Solo conceptos de aplicabilidad general revisada, sin convertir cifras de un simulador en universales | Fuente pendiente de selección |

Objetivo: al menos tres documentos sustanciales y unas 20 páginas equivalentes, con contenido útil para los tres simuladores y al menos un caso demostrable por simulador. El mínimo de volumen global no garantiza cobertura suficiente de cada uno: registrar también las lagunas.

No contar una página de catálogo ni unas notas de versión breves como un manual completo. Guardar texto limpio en `.md` o `.txt`, o PDF con texto seleccionable. Revisar tablas e imágenes que contengan información necesaria antes de usarlas para responder.

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
