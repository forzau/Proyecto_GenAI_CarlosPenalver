# Contexto de trabajo

- Proyecto de Carlos Peñalver para el módulo de IA Generativa del máster.
- Trabajar en español. Priorizar que el alumno pueda explicar cada decisión.
- En cada sesión de trabajo, proponer cuando sea posible una tarea concreta que el alumno pueda hacer en paralelo. Explicar para qué sirve y continuar las tareas independientes mientras la realiza.
- Esta carpeta es la raíz del repositorio. `../Notebooks/` contiene referencias de clase: no modificar ni copiar su entorno o sus credenciales.
- Leer README.md y docs/PLAN.md antes de desarrollar. Actualizar el estado al completar entregables.
- Dominio confirmado: ingeniero de boxes para simracing. El diseño cubrirá diagnóstico general e iRacing, Assetto Corsa Competizione (ACC) y Le Mans Ultimate (LMU); la cobertura demostrable depende del corpus. No asumir todos los coches o versiones.
- Stack obligatorio: Gemini para LLM y embeddings, ChromaDB y LangGraph sobre LangChain. Notebook obligatorio; Streamlit es el bonus previsto.
- Mantener el núcleo compartido por notebook y web cuando se implemente. Crear módulos solo cuando exista lógica que compartir.
- No añadir otros proveedores, agentes múltiples, servicios ni infraestructura para este MVP.
- Nunca versionar .env, claves, índices, datos de empresa o conversaciones privadas. Revisar las salidas de los notebooks antes de subirlas.
- No llamar a Gemini en las pruebas de setup. Las evaluaciones reales se ejecutan explícitamente y se documentan, con su coste si se conoce.
- No presentar plantillas ni respuestas inventadas como resultados. Comprobar las citas contra los fragmentos recuperados.
- Filtrar la recuperación por simulador y aplicabilidad del documento; no trasladar valores o ajustes entre simuladores, coches o versiones. No inventar telemetría, reglajes disponibles ni mejoras en pista.
- Una sesión conserva síntomas, condiciones, recomendaciones y cambios confirmados por el piloto. Al cambiar simulador o coche, pedir confirmar el nuevo contexto y descartar los reglajes anteriores como estado vigente.
- Hacer las pruebas adecuadas a cada cambio. Al implementar recuperación y memoria, probar los límites con datos locales y añadir una comprobación pequeña de su comportamiento.
