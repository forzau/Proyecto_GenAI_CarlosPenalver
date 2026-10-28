# Ingeniero de boxes para simracing

Dominio confirmado por el alumno el 22/10/2026. El diseño cubrirá diagnóstico general e iRacing, Assetto Corsa Competizione (ACC) y Le Mans Ultimate (LMU). El MVP utiliza las tres guías elegidas por el alumno, con 75 fichas documentales; no hay coches ni versiones validados en pista. Véase FUENTES.md.

## Usuario y problema

Un piloto de simracing describe el comportamiento del coche y necesita saber qué información falta, qué hipótesis considerar y qué cambio merece probar. El asistente debe explicar la recomendación con fuentes y continuar la sesión cuando el piloto comunica el resultado.

## Experiencia disponible y orden de trabajo

El alumno solo ha jugado LMU, principalmente un Ferrari GT3 cuyo modelo exacto no recuerda. El Ferrari le resultaba más estable para empezar y recuerda otros coches difíciles y sobreviraje difícil de recuperar. Son impresiones históricas sin versión ni condiciones identificadas; no una medición ni una conclusión sobre la física actual. Empezaremos por consultas documentales de LMU, este relato incompleto y escenarios hipotéticos explícitos. iRacing y ACC siguen en el alcance previsto; se incorporarán a las pruebas según la evidencia disponible, sin exigir que el alumno haya jugado a ellos.

El alumno puede evaluar claridad y utilidad de la conversación. La corrección técnica se revisará contra fuentes aplicables, y las mejoras de rendimiento requerirían pruebas en pista. No convertir una opinión de utilidad en validación de un setup.

Si la cobertura especializada resulta insuficiente, la alternativa a valorar será un experto en fundamentos generales de simracing con RAG, manteniendo un dominio definido para la entrega. No se cambia automáticamente a un chatbot de cualquier tema ni se reutilizan fuentes específicas como universales. Esta alternativa queda pendiente de decidir si aparece esa limitación.

## Alcance de una semana

- Interpretar subviraje, sobreviraje, inestabilidad en frenada y pérdida de tracción, considerando entrada, mitad y salida de curva.
- Preguntar por el contexto relevante antes de recomendar ajustes concretos.
- Recuperar documentación del simulador seleccionado y documentación general de aplicabilidad revisada.
- Explicar ajustes documentados de neumáticos, frenos, suspensión, diferencial o aerodinámica; no se promete cubrirlos todos para cada coche.
- Proponer un cambio principal cada vez, con motivo, observación esperada y criterio para conservarlo o revertirlo.
- Recordar recomendaciones, cambios realmente aplicados y observaciones del piloto durante la conversación.
- Conservar fuentes para revisión en el notebook y preparar Streamlit con detección conversacional de simulador, memoria por sesión y respuestas limpias; sin selector manual por ahora.

Fuera del MVP: telemetría en directo, análisis automático de archivos de telemetría, voz o radio, modificación de archivos de setup, conexión con el juego, optimización automática, estrategia completa de resistencia y promesas de mejora de tiempos.

## General frente a específico

Si no hay simulador indicado ni contexto confirmado, el agente pregunta antes de diagnosticar. Para simuladores fuera de LMU/iRacing/ACC ofrece orientación general con aviso de falta de especialidad, sin consultar ni trasladar documentos del corpus. Los valores, rangos y ajustes concretos necesitan evidencia aplicable al simulador, coche, versión y condiciones. Si falta, el agente explica la limitación o pide los datos necesarios en lugar de trasladar recomendaciones de otro entorno.

Usaremos un solo agente y un único grafo. Los metadatos y filtros de recuperación delimitan el contexto antes de generar la respuesta; el prompt añade comprobaciones de aplicabilidad. Los documentos de iRacing no se etiquetarán como generales para usarlos en ACC o LMU.

Objetivo de demo: al menos un caso respaldado de cada simulador, un seguimiento de sesión y una consulta sin evidencia suficiente. Esto no equivale a cubrir todos sus coches y versiones.

## Contexto mínimo de una sesión

Recoger progresivamente solo lo necesario para la consulta:

- Simulador, versión si afecta a la respuesta, coche y categoría.
- Circuito o tipo de curva, fase y velocidad aproximada del problema.
- Condiciones relevantes: seco/mojado, temperaturas, combustible, neumáticos y vueltas de calentamiento, si se conocen.
- Setup de partida, restricciones fixed/open y valores actuales relevantes, con unidades.
- Síntoma descrito, cambios confirmados por el piloto y resultado observado.

Un dato desconocido se mantiene como desconocido. Una recomendación no se registra como aplicada hasta que lo diga el piloto. Cambiar de simulador o coche obliga a revisar el contexto y evita arrastrar reglajes como si siguieran vigentes.

## Utilidad que debemos comprobar

1. Recomendaciones ligadas a documentos aplicables, con citas verificables.
2. Reconocimiento de información ausente y límites de cobertura.
3. Coherencia entre turnos al registrar una prueba de ajuste.
4. Separación entre diagnóstico general y parámetros específicos de cada simulador.

El modelo base puede resolver bien preguntas generales. RAG puede fallar si recupera una versión antigua o un coche equivocado. No se afirma superioridad frente al modelo base; el alumno descartó esa comparación.

## Caso de demo

El piloto identifica simulador y coche y describe subviraje en una fase concreta. El agente solicita el dato imprescindible que falte, recupera fuentes y propone una prueba. El piloto confirma si la aplicó y relata el resultado. El agente revisa el diagnóstico conservando el contexto. Al cambiar de simulador, no reutiliza cifras anteriores.

Los diálogos de prueba serán escenarios ficticios identificados como tales. Las mejoras reales en pista solo se documentarán si el alumno las prueba; una respuesta coherente no demuestra por sí sola mejora de rendimiento.

## Decisiones pendientes

- Preparar la indexación y consultas de demo basadas en las guías ya seleccionadas. No es necesario fijar un coche para explicar sus recomendaciones cualitativas; declarar los límites de aplicación.
- Confirmar fecha y hora exactas de entrega y cuota o presupuesto de Gemini para las pruebas.
