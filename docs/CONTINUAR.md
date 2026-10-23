# Continuar en otro equipo

Cierre de sesión: 23/10/2026. Rama de trabajo: **`setup-inicial`**.

## Punto de partida

- Corpus cerrado: Ultimate Setup Hub para LMU (25 fichas), chuleta Chris Haye para iRacing (20) y Driver61 V1 para ACC (30). No ampliar las fuentes para este MVP.
- 75 fichas indexadas con `gemini-embedding-2`, 3072 dimensiones y distancia coseno en Chroma. Colección: `simracing_1809b2209d21ea5366b5`.
- Tres consultas reales recuperaron su ficha esperada entre los tres primeros resultados, sin mezclar simuladores. Resultados en [EVALUACION.md](EVALUACION.md) y en el informe local.
- Notebook simplificado: configuración, carga, embeddings, índice y una búsqueda de ejemplo. Sin asserts ni celdas de validación. La búsqueda de ejemplo quedó sin repetir para ahorrar API.
- Agente, memoria, chat, comparación con modelo base y Streamlit todavía pendientes. No hay respuestas generadas por el agente ni pruebas de reglajes en pista.

## Recuperar código y datos

El código está en [GitHub, rama setup-inicial](https://github.com/forzau/Proyecto_GenAI_CarlosPenalver/tree/setup-inicial). En una carpeta nueva:

```powershell
git clone --branch setup-inicial https://github.com/forzau/Proyecto_GenAI_CarlosPenalver.git
cd Proyecto_GenAI_CarlosPenalver
```

Si ya existe una copia, guardar primero cualquier trabajo propio y actualizar la rama con `git pull --ff-only`.

**Una clonación no incluye el corpus ni el índice.** En el equipo anterior se ha preparado:

`Proyecto/outputs/continuar_otro_equipo_2026-10-23.zip`

Trasladar ese ZIP por un medio privado y extraer su contenido en la raíz de la nueva copia del repositorio, conservando las rutas:

| Ruta restaurada | Contenido |
| --- | --- |
| `data/corpus/mvp/` | Originales, transcripciones y las 75 fichas en JSONL |
| `data/chroma/` | Copia del índice persistente para evitar regenerar embeddings |
| `outputs/retrieval_evaluation.json` | Resultados de las tres consultas ya realizadas |
| `outputs/requirements-session.txt` | Versiones completas instaladas en esta sesión de Windows |
| `outputs/traslado_manifest.json` | Archivos del paquete y huellas SHA-256 |

El ZIP queda fuera de Git y **no contiene `.env`, claves ni `.venv`**. Los originales de terceros siguen siendo copias locales; no subirlos al repositorio. Las seis fuentes antiguas de reserva no hacen falta para continuar.

También se pueden copiar directamente esas carpetas y el informe desde el equipo anterior. Si se hace mediante OneDrive, asegurarse de que los archivos están descargados antes de abrirlos. Cerrar los kernels que utilicen Chroma antes de copiar una versión posterior del índice. Restaurar en una carpeta nueva si el equipo de destino ya contiene otro índice.

## Preparar el entorno

En Windows, usar Python 3.12 y crear un entorno nuevo; no trasladar `.venv`:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r outputs/requirements-session.txt
Copy-Item .env.example .env
```

La lista completa corresponde a Windows. Para otro sistema operativo, empezar con `requirements.txt` y sus versiones directas; la portabilidad a ese sistema aún no se ha comprobado. No sobrescribir un `.env` existente.

Configurar **localmente**:

- `GOOGLE_API_KEY`: clave propia de Google AI Studio; recuperar la del equipo anterior por un medio privado si se desea reutilizarla. No pegarla en el chat ni publicarla.
- `GEMINI_EMBEDDING_MODEL=gemini-embedding-2`.
- `GEMINI_MODEL`: dejar pendiente hasta elegir el modelo de generación en la siguiente fase.

Abrir `notebooks/proyecto.ipynb` con el kernel `.venv` del nuevo equipo. El código usa rutas relativas a la raíz del repositorio, no la ruta personal del equipo anterior. El `.env` del proyecto tiene prioridad sobre las variables heredadas del sistema.

Con el índice restaurado, abrirlo reutiliza las 75 fichas y no genera nuevos embeddings del corpus. Ejecutar la celda de búsqueda sí consume un embedding de consulta. No ejecutar búsquedas ni `scripts/evaluate_retrieval.py` solo para comprobar el traslado.

Las pruebas locales están fuera del notebook y no llaman a Gemini:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Si falta el JSONL, `scripts/build_corpus.py` lo reconstruye a partir de los originales y transcripciones restaurados, sin API. Si falta Chroma, la primera indexación necesitará generar otra vez los embeddings: recuperar el ZIP antes de hacerlo.

## Siguiente sesión

1. Leer `AGENTS.md`, este documento y [PLAN.md](PLAN.md). Mantener el notebook directo y las pruebas en `tests/` o scripts explícitos.
2. Revisar los ejemplos de clase `clase_LangGraph.ipynb` y `clase_agentes.ipynb` para seguir su estilo. Están en `../Notebooks/`, fuera del repositorio y del ZIP; pueden estar disponibles en la carpeta de clase de OneDrive. El código actual funciona sin ellos.
3. Elegir un LLM de Gemini disponible dentro del uso gratuito acordado e implementar el flujo pregunta → recuperación filtrada por simulador → respuesta con fuentes.
4. Añadir memoria por conversación, distinguiendo cambios propuestos y confirmados. Después, chat en notebook con cinco respuestas reales; Streamlit al final como bonus.

Reutilizar `retrieval.py`. Su adaptación a Embedding 2 depende de la integración 4.4.2; no actualizar dependencias ni cambiar el modelo de embeddings por rutina. El MVP usa recuperación síncrona.

El alumno prefiere código parecido a clase, alcance básico y pocas llamadas de API. Cuando haya una tarea útil en paralelo, proponérsela sin bloquear el avance. No dispone del simulador en casa: evaluar fidelidad documental, citas y memoria; no prometer mejoras de rendimiento ni vigencia física de las guías.
