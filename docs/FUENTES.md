# Fuentes y corpus

## Candidatas para Power BI

Estos enlaces se han comprobado al preparar el setup. Son candidatos, no documentos descargados ni indexados. Registrar la versión o fecha de consulta de la copia que finalmente se use. No hace falta abarcar toda la documentación de Power BI.

| ID | Fuente | Uso previsto | Estado |
| --- | --- | --- | --- |
| MS01 | [Microsoft: esquema en estrella](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema) | Hechos, dimensiones y granularidad | Seleccionar secciones y guardar copia local |
| MS02 | [Microsoft: relaciones del modelo](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-relationships-understand) | Propagación de filtros y relaciones | Seleccionar secciones y guardar copia local |
| MS03 | [Microsoft: CALCULATE](https://learn.microsoft.com/en-us/dax/calculate-function-dax) | Contexto de filtros y ejemplos de la función | Seleccionar secciones y guardar copia local |
| PROPIO01 | Diccionario del modelo de ventas ficticio | Tablas, relaciones y medidas propias | Pendiente de autoría |

Objetivo: al menos tres documentos sustanciales y unas 20 páginas equivalentes, comprobando volumen útil después de limpiar menús y navegación. Para fuentes web, guardar texto limpio en `.md` o `.txt`; no asumir que tres páginas breves cumplen el volumen. Si se exportan a PDF, comprobar que conservan texto seleccionable.

## Registro al incorporar cada documento

Anotar ID, título, autor, URL original o procedencia, fecha/versión, archivo local, idioma, extensión útil, permiso/licencia y limpieza realizada. Si no se puede redistribuir, indicar cómo obtenerlo legalmente en lugar de subirlo.

Cada fragmento debe conservar ID de documento, título, URL, fecha/versión, sección o página e identificador de fragmento. Si cambia el modelo de embeddings o la segmentación, reconstruir el índice y registrar la configuración utilizada.

Los documentos se guardarán en `data/corpus/` y el índice en `data/chroma/`, ambos excluidos de Git. La documentación del corpus sí debe permitir reproducirlo.

## Referencias locales de clase

| Notebook en ../Notebooks/ | Qué reutilizar como referencia |
| --- | --- |
| rag_profesor.ipynb y clase3.ipynb | Carga de PDF, chunking, Chroma y recuperación; usar Gemini Embeddings según el enunciado |
| clase_LangGraph.ipynb | Estado, nodos, aristas y flujo del grafo |
| clase_agentes.ipynb | Historial, mensajes y checkpointer de memoria |
| clase2.ipynb | Configuración de Gemini y composición de prompts |

Son referencias de aprendizaje. No copiar sus claves, sus bases vectoriales ni sus salidas a este proyecto.
