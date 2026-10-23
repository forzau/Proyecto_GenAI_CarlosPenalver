# Corpus del MVP

Selección confirmada por el alumno el 23/10/2026: tres fuentes, una por simulador. La fase de búsqueda queda cerrada para esta entrega. No necesitamos acceso al simulador para preparar y evaluar un asistente documental.

| ID | Fuente elegida | Preparación | Fichas |
| --- | --- | --- | --- |
| LMU_USH | [Ultimate Setup Hub — Race Engineer](https://ultimatesetuphub.com/race-engineer) | Captura del árbol público: 38 páginas visitadas, 25 hojas de diagnóstico; se excluyen navegación, formularios y Eva | 25 |
| IR_CHRIS_HAYE | [Chuleta de Chris Haye reproducida por SimRacingCockpit](https://simracingcockpit.gg/improving-your-car-setup-in-iracing/) | Transcripción visual de las celdas de la imagen; no se indexa el artículo completo | 20 |
| ACC_DRIVER61 | [Driver61 ACC Setup Guide V1](https://driver61.com/wp-content/uploads/2021/04/Driver61-Assetto-Corsa-Competizione-Setup-Guide-V1.pdf) | Transcripción visual de una página larga, separando columnas, problemas y condiciones | 30 |

**Resultado: 75 fichas documentales, todavía sin embeddings ni índice Chroma.** Hay tres fuentes, no 75 documentos originales. La imagen y la lámina PDF no se contabilizan artificialmente como decenas de páginas. El inventario activo es [corpus_mvp.json](corpus_mvp.json), con autor, procedencia, método, rutas y huellas SHA-256.

## Qué contiene cada ficha

Una ficha corresponde a un problema completo y conserva su contexto: fase de curva, velocidad, condición, alternativas y notas. Incluye `id`, `source_id`, `simulator`, `title`, `locator`, `url`, `game_version`, `limitation` y `text`. Las hojas de LMU enlazan a su URL concreta; las transcripciones identifican la celda y, en ACC, la página 1.

Usaremos cada ficha como fragmento inicial: evita separar el síntoma de los ajustes o confundir alternativas OR con cambios acumulativos. La recuperación filtrará por `simulator`. Las respuestas de evaluación y los recuerdos del alumno quedan fuera del corpus.

## Límites aceptados para esta entrega

- Son guías orientativas, no configuraciones verificadas en pista. Se evaluará fidelidad documental, recuperación, citas y memoria; no ganancias de rendimiento.
- La chuleta de Chris Haye es general y está publicada en un artículo de iRacing fechado el 19/05/2023. Se asigna a iRacing por la selección del proyecto, sin afirmar que describa los ajustes disponibles en todos sus coches.
- El PDF de ACC es V1 y está en una ruta de publicación de abril de 2021. No demuestra vigencia para la física actual. Contiene afirmaciones que pueden resultar discutibles: transcribirlas no las valida.
- La captura de LMU es del 23/10/2026; fecha de captura no equivale a versión de juego. No se ha utilizado la herramienta generativa Eva como fuente.
- Coche y versión del juego no constan de forma suficiente: se registra `unknown`. El agente podrá explicar lo que recomienda la guía con esa limitación; no necesita bloquear una explicación cualitativa hasta conocer todos los datos.
- Se conservan las condiciones y advertencias de los originales. La broma PICNIC de la lámina de iRacing se identifica como nota humorística, no como diagnóstico del usuario.

No se ha identificado una licencia que permita redistribuir los originales y sus transcripciones. Permanecen en local y fuera de Git, junto con el corpus generado. El repositorio contiene el inventario, el método y el constructor.

## Archivos y reproducción local

```text
data/corpus/mvp/
├── originales/
│   ├── lmu_pages.json
│   ├── iracing_cheatsheet.jpg
│   └── acc_driver61_v1.pdf
└── preparado/
    ├── iracing_cheatsheet.md
    ├── acc_driver61_v1.md
    └── corpus.jsonl
```

Desde `Proyecto`, con los archivos locales presentes:

```powershell
.\.venv\Scripts\python.exe scripts/build_corpus.py
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

El constructor verifica las huellas del inventario, rechaza capturas incompletas o fichas vacías y reúne las 75 fichas en JSONL. Si se cambia una transcripción, revisarla antes de actualizar su huella en el inventario. No llama a Gemini.

Para volver a obtener los originales:

1. LMU: abrir el árbol público y recorrer sus enlaces de diagnóstico. En cada hoja guardar URL, ruta de decisiones, título, texto y HTML del bloque que contiene el encabezado principal. La captura local incluye `visited`, `pending`, `errors` y `pages`; una captura completa no debe dejar pendientes ni errores. Se realizó desde el DOM de un navegador porque la página carga el contenido dinámicamente.
2. iRacing: descargar la [imagen enlazada desde el artículo](https://simracingcockpit.gg/wp-content/uploads/2023/05/iracing-setup-cheat-sheet.jpg) y transcribir cada celda en un apartado Markdown `##`, conservando condiciones y alternativas.
3. ACC: descargar el PDF y revisar visualmente sus zonas. El texto extraído directamente mezcla columnas: por eso cada celda se transcribió a un apartado `##` en lugar de usar esa extracción.

La nueva obtención y la transcripción visual requieren revisión manual; no se promete reconstrucción automática idéntica desde una clonación vacía. Las huellas permiten comprobar las copias usadas en esta entrega.

## Material anterior en reserva

Las seis copias de `data/corpus/pendientes/` y [corpus.json](corpus.json) son un archivo de fuentes candidatas, fuera del corpus activo. Las revisiones [IR04](REVISION_IR04.md) y [Ultimate Setup Hub](REVISION_USH.md) conservan la exploración anterior; no amplían la selección actual.

## Referencias de clase

`../Notebooks/rag_profesor.ipynb` y `clase3.ipynb`: carga, Chroma y recuperación. `clase_LangGraph.ipynb`: grafo. `clase_agentes.ipynb`: memoria. `clase2.ipynb`: Gemini y prompts. No copiar claves, índices ni salidas del entorno de clase.
