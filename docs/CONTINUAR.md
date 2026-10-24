# Continuar en otro equipo

## Copia de trabajo local de este equipo (24/10/2026)

La copia activa está en `C:\Users\forza\Projects\Proyecto_GenAI_CarlosPenalver`, fuera de OneDrive. El código se ha recuperado de la rama `setup-inicial` y los datos del ZIP descargado desde OneDrive web; todas las huellas del inventario coinciden. La configuración privada se ha restaurado sin publicar la clave. El documento `docs/PLAN.md` conserva las anotaciones locales de esta sesión.

Entorno Python 3.12.10 instalado y comprobado: dependencias sin conflictos, 31 pruebas locales superadas y 75 fichas accesibles en Chroma. Consultas vectoriales locales comprobadas para los tres simuladores sin API. Seleccionar el kernel `Python 3.12 (Proyecto Simracing)`, que apunta a `.venv` de esta copia. No hace falta reinstalar ni regenerar embeddings.

La carpeta anterior de OneDrive se conserva. Su sincronización se reinició y restableció, pero seguía devolviendo `0x8007017C` al leer los archivos solo en la nube. No utilizarla como copia de trabajo mientras siga ese problema. El diagnóstico registra más de 500.000 archivos.

Los notebooks de clase siguen en `C:\Users\forza\OneDrive - UMH\Máster\IA Generativa\Notebooks`; no están en `../Notebooks` respecto a esta nueva copia. No copiar su entorno ni sus credenciales. La disponibilidad de esas referencias depende de OneDrive.

Cierre de sesión: 24/10/2026. Rama de trabajo: **`setup-inicial`**.

## Punto de partida

- Corpus cerrado: Ultimate Setup Hub para LMU (25 fichas), chuleta Chris Haye para iRacing (20) y Driver61 V1 para ACC (30). No ampliar las fuentes para este MVP.
- 75 fichas indexadas con `gemini-embedding-2`, 3072 dimensiones y distancia coseno en Chroma. Colección: `simracing_1809b2209d21ea5366b5`.
- Tres consultas reales recuperaron su ficha esperada entre los tres primeros resultados, sin mezclar simuladores. Resultados en [EVALUACION.md](EVALUACION.md) y en el informe local.
- Notebook funcional: configuración, corpus, embeddings, índice, agente, memoria, chat y cinco casos reales guardados. Sin asserts ni celdas de validación. No ejecutar consultas solo para comprobar el traslado.
- RAG con memoria temporal y chat en notebook implementados en la copia local. `InMemorySaver`, identificador por conversación y confirmación al cambiar de contexto. Hay 31 pruebas locales, arranque del chat comprobado con un kernel real sin API, y cinco casos documentados con LMU, iRacing, ACC, seguimiento y cifra exacta no disponible. Ejemplos guardados en Markdown; demostraciones ejecutables convertidas en ejemplos opcionales. Pendientes revisión del notebook, mejoras de fidelidad y Streamlit. Sin pruebas en pista. El código y la documentación de esta sesión se guardan en la rama `setup-inicial`; el corpus, el índice y los informes privados se trasladan en el paquete local.

## Recuperar código y datos

El código está en [GitHub, rama setup-inicial](https://github.com/forzau/Proyecto_GenAI_CarlosPenalver/tree/setup-inicial). En una carpeta nueva:

```powershell
git clone --branch setup-inicial https://github.com/forzau/Proyecto_GenAI_CarlosPenalver.git
cd Proyecto_GenAI_CarlosPenalver
```

Si ya existe una copia, guardar primero cualquier trabajo propio y actualizar la rama con `git pull --ff-only`.

**Una clonación no incluye el corpus ni el índice.** Antes de cambiar de equipo, trasladar por un medio privado el ZIP siguiente y, por separado, el archivo `.env` de la raíz del proyecto. No depender de la copia bloqueada de OneDrive. Paquete de esta sesión:

`outputs/continuar_otro_equipo_2026-10-24.zip` (dentro de la copia local activa)

Trasladar ese ZIP por un medio privado y extraer su contenido en la raíz de la nueva copia del repositorio, conservando las rutas:

| Ruta restaurada | Contenido |
| --- | --- |
| `data/corpus/mvp/` | Originales, transcripciones y las 75 fichas en JSONL |
| `data/chroma/` | Copia del índice persistente para evitar regenerar embeddings |
| `outputs/*evaluation*.json`, `outputs/agent_*.json` | Recuperación, generaciones y revisiones reales de esta sesión y las anteriores |
| Código, notebook y documentación | Copia exacta del commit indicado en el manifiesto |
| `outputs/repositorio_2026-10-24.bundle` | Historial Git y rama para recuperación sin red |
| PDF del enunciado en la raíz | Referencia docente local, fuera de GitHub |
| `outputs/requirements-session.txt` | Versiones completas instaladas en esta sesión de Windows |
| `outputs/traslado_manifest.json` | Archivos del paquete y huellas SHA-256 |

El ZIP queda fuera de Git y **no contiene `.env`, claves ni `.venv`**. Los originales de terceros siguen siendo copias locales; no subirlos al repositorio. Las seis fuentes antiguas de reserva no hacen falta para continuar.

El manifiesto identifica el commit y las huellas SHA-256 de todos los archivos. El ZIP también contiene el código por si GitHub no estuviera disponible; en ese caso puede extraerse en una carpeta nueva. El bundle permite recuperar Git con `git clone --branch setup-inicial RUTA_AL_BUNDLE CARPETA_NUEVA`, y después se extrae el ZIP en esa carpeta. El paquete del 23/10 se conserva como copia anterior.

También se pueden copiar directamente esas carpetas y los informes desde el equipo anterior. Si se hace mediante OneDrive, asegurarse de que los archivos están descargados antes de abrirlos. Cerrar los kernels que utilicen Chroma antes de copiar una versión posterior del índice. Restaurar en una carpeta nueva si el equipo de destino ya contiene otro índice.

## Preparar el entorno

En Windows, usar Python 3.12 y crear un entorno nuevo; no trasladar `.venv`:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r outputs/requirements-session.txt
# Solo si no se ha trasladado el .env privado:
Copy-Item .env.example .env
```

La lista completa corresponde a Windows. Para otro sistema operativo, empezar con `requirements.txt` y sus versiones directas; la portabilidad a ese sistema aún no se ha comprobado. No sobrescribir un `.env` existente.

Configurar **localmente**:

- `GOOGLE_API_KEY`: clave propia de Google AI Studio; recuperar la del equipo anterior por un medio privado si se desea reutilizarla. No pegarla en el chat ni publicarla.
- `GEMINI_EMBEDDING_MODEL=gemini-embedding-2`.
- `GEMINI_MODEL=gemini-3.1-flash-lite`: modelo de generación elegido por la disponibilidad indicada por el alumno; no cambiarlo automáticamente si se agota la cuota.

Abrir `notebooks/proyecto.ipynb` con el kernel `.venv` del nuevo equipo. El código usa rutas relativas a la raíz del repositorio, no la ruta personal del equipo anterior. El `.env` del proyecto tiene prioridad sobre las variables heredadas del sistema.

Con el índice restaurado, abrirlo reutiliza las 75 fichas y no genera nuevos embeddings del corpus. Ejecutar la configuración hasta crear `app` y después las funciones e inicio del chat de la sección 6. Las demostraciones de las secciones 4 y 5 son bloques opcionales; leer los ejemplos guardados no consume API. Cada mensaje normal del chat hace una búsqueda y una generación, salvo cuando pide confirmación. `/nuevo` empieza otra conversación; `/salir` cierra el chat. La memoria se pierde al reiniciar el kernel o recrear `app`. No ejecutar consultas ni evaluaciones solo para comprobar el traslado.

Las pruebas locales están fuera del notebook y no llaman a Gemini:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Si falta el JSONL, `scripts/build_corpus.py` lo reconstruye a partir de los originales y transcripciones restaurados, sin API. Si falta Chroma, la primera indexación necesitará generar otra vez los embeddings: recuperar el ZIP antes de hacerlo.

## Siguiente sesión

1. Leer `AGENTS.md`, este documento y [PLAN.md](PLAN.md). Mantener el notebook directo y las pruebas en `tests/` o scripts explícitos.
2. Retomar las propuestas de mejora del alumno sobre el notebook. Después implementar la web en Streamlit sobre `agent.py` y `retrieval.py`, con memoria por sesión y `respuesta_piloto` sin citas visibles. La web aún no está implementada. Los ejemplos de clase son referencias opcionales externas; el código actual funciona sin ellos.
3. Revisar el chat, la memoria y los cinco casos del notebook. El informe agregado está en `outputs/evaluation_cases.json`; se conservan los informes de etapas anteriores. `scripts/evaluate_cases.py` no usa API sin `--run` y reutiliza resultados ya completados. No repetir llamadas por rutina. La ficha contradictoria `LMU_USH_08` se excluye del consejo mediante `prompts/source_quality.json` sin cambiar el corpus ni sus embeddings.
4. El alumno está revisando el notebook para proponer mejoras. Revisar después la fidelidad restante y continuar con Streamlit y presentación. La comparación sin RAG se descartó por decisión del alumno el 24/10/2026; no figura como requisito en el enunciado.

Reutilizar `retrieval.py`. Su adaptación a Embedding 2 depende de la integración 4.4.2; no actualizar dependencias ni cambiar el modelo de embeddings por rutina. El MVP usa recuperación síncrona.

El alumno prefiere código parecido a clase, alcance básico y pocas llamadas de API. Cuando haya una tarea útil en paralelo, proponérsela sin bloquear el avance. No dispone del simulador en casa: evaluar fidelidad documental, citas y memoria; no prometer mejoras de rendimiento ni vigencia física de las guías.

Presentación acordada: mantener citas visibles en el notebook para evaluación; la futura web mostrará `resultado["respuesta_piloto"]`, sin referencias. El núcleo conserva `respuesta` original, `fuentes` y `documentos` para revisión interna. La separación de presentación está incluida en las 31 pruebas locales actuales y no consume API.

La memoria actual conserva mensajes literales con roles; no existe un registro estructurado independiente de ajustes aplicados. La interpretación de lo confirmado depende de Gemini. Las pruebas locales cubren aislamiento y cambios de contexto, y las dos pruebas reales muestran continuidad; la fidelidad técnica de sus respuestas sigue siendo parcial. Para cambios de contexto usar los campos explícitos y `confirmar_contexto=True`; una mención en texto no cambia automáticamente el filtro.

## Cierre del 24/10/2026

Próxima sesión acordada: propuestas de mejora del notebook y web en Streamlit. No hacer la comparación sin RAG. Se conserva la configuración Gemini 3.1 Flash-Lite, temperatura 1.0, siguiendo la recomendación del proveedor para Gemini 3; no se ha demostrado que sea óptima mediante un experimento de temperaturas. La fidelidad documental sigue siendo parcial, como detalla EVALUACION.md.

El ZIP no conserva conversaciones activas: la memoria de `InMemorySaver` es temporal. Los ejemplos documentados y sus informes sí se incluyen. No instalar dependencias ni regenerar embeddings en este equipo por rutina. En otro equipo, crear su propia `.venv` con Python 3.12 y las versiones guardadas.
