# Contexto del alumno y preguntas para la demo

## Información confirmada el 23/10/2026

| Simulador | Experiencia del alumno | Observaciones fiables disponibles |
| --- | --- | --- |
| iRacing | No ha jugado | No hay experiencias propias que registrar |
| ACC | No ha jugado | No hay experiencias propias que registrar |
| LMU | Ha jugado principalmente GT3; modelo concreto pendiente | Recuerda sobreviraje frecuente y dificultad para recuperarlo; impresión histórica sin datos medidos |

Esta situación no bloquea el proyecto: empezaremos con consultas y escenarios basados en documentación. No se atribuirán al alumno pruebas, cambios o resultados que no haya realizado.

## Primer relato de referencia: sobreviraje en GT3

El alumno recuerda LMU como exigente: conducía principalmente GT3, los coches sobreviraban con facilidad y le resultaba difícil recuperar el sobreviraje. Se registra como experiencia subjetiva de una época no identificada, no como una afirmación comprobada sobre la versión actual.

Datos desconocidos: modelo de coche, versión, circuito, fase de curva, estado de neumáticos, condiciones, reglaje y acciones de conducción. No hay cambios de setup ni resultados comparables confirmados.

La primera prueba del agente será reconocer esa falta de contexto y preguntar de forma breve por el coche y si ocurría al frenar, en apoyo o al acelerar. No deberá elegir una causa, prescribir un ajuste ni asumir que se trataba de sobreviraje bajo potencia. El ejemplo de sesión queda fuera del corpus de conocimiento.

## Tarea en paralelo

Si recuerda el modelo o marca del GT3, indicarlo. No necesita volver a jugar ni reconstruir condiciones que no recuerda. Podemos seguir revisando fuentes con la categoría GT3 y dejar los demás datos como desconocidos.

Más adelante podrá probar la conversación del asistente y valorar si entiende la explicación, si las preguntas de contexto tienen sentido y si la respuesta le ayuda a decidir qué información consultar. Esta valoración no equivale a validar técnicamente el reglaje.

## Cómo construiremos las pruebas

- Las preguntas de conocimiento partirán de fuentes identificadas y tendrán criterios de revisión documental.
- Los escenarios de diagnóstico y seguimiento serán hipotéticos y se etiquetarán así, sin presentarlos como vueltas reales.
- Las respuestas del agente se guardarán únicamente después de ejecutarlo; no se inventarán resultados para completar la entrega.
- No se afirmará una mejora de rendimiento sin una prueba real comparable.
- Las respuestas de referencia quedan fuera del corpus. Gemini sin RAG y el agente recibirán el mismo contexto de usuario.

Los primeros candidatos de preguntas sobre LMU están en [EVALUACION.md](EVALUACION.md). La elección de coches no bloquea la limpieza de los documentos ya disponibles.
