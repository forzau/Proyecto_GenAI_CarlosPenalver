# Despliegue privado de BOX en Streamlit Community Cloud

Aplicación: [BOX](https://box-ingeniero-pista.streamlit.app/), con acceso privado y Python 3.12. Si el contenedor de Community Cloud se queda en el indicador de carga, la [ruta directa de BOX](https://box-ingeniero-pista.streamlit.app/~/+/) permite abrir la aplicación con la misma sesión autorizada. Ambas rutas se han comprobado sin sesión y bloquean el acceso.

## Archivos necesarios

El repositorio contiene el código y `.streamlit/secrets.example.toml`, sin credenciales. El autor conserva aparte `box_datos_privados_2026-10-28.json.gz`, correspondiente al manifiesto publicado. Contiene solo las 75 fichas y sus vectores, sin PDFs originales, clave ni conversaciones. No subirlo a GitHub: las fuentes no tienen una licencia de redistribución identificada y se mantienen privadas.

## Pasos

1. Entrar en [Streamlit Community Cloud](https://share.streamlit.io/). El titular completa el inicio de sesión y acepta las condiciones del servicio.
2. Crear una aplicación desde `forzau/Proyecto_GenAI_CarlosPenalver`, rama `main`, archivo `app.py`. En **Advanced settings**, seleccionar **Python 3.12**. No añadir todavía la clave de Gemini.
3. Desplegar. La pantalla pedirá el paquete privado; sin clave y sin datos no hay llamadas a Gemini.
4. En **App settings → Sharing → Who can view this app**, elegir **Only specific people can view this app**. Conservar solo tu cuenta durante las pruebas y la presentación. Un repositorio público no hace privada la app automáticamente. Community Cloud admite una app privada por espacio de trabajo.
5. Solo después, en **App settings → Secrets**, copiar la plantilla y sustituir el marcador por la clave de Google. Mantener las tres variables como valores de primer nivel de TOML, sin sección adicional: Streamlit las expone como variables de entorno. No pegar claves en GitHub, en el chat ni en campos normales de la app.
6. Abrir BOX con tu sesión autorizada y cargar `box_datos_privados_2026-10-28.json.gz`. Se comprueba SHA-256 y se reconstruye Chroma con los vectores guardados: **cero llamadas de embeddings del corpus**.
7. Enviar una consulta LMU y un seguimiento; cambiar de modelo y abrir otra sesión para revisar continuidad y aislamiento. Comprobar «Nueva conversación» y una consulta sin simulador. Estas consultas reales sí consumen API.
8. Abrir la URL sin iniciar sesión y comprobar que Streamlit exige acceso antes de mostrar BOX. No compartir el enlace hasta verificar ese bloqueo.

El disco del servidor no es un respaldo. Si un reinicio o reconstrucción elimina los datos locales, BOX volverá a pedir el paquete. Conservarlo a mano el día de la presentación. Las conversaciones tampoco sobreviven a un reinicio. El arranque nunca recalcula los embeddings del corpus.

La plataforma gestiona dirección y puerto del servidor. Para ejecutar localmente con acceso solo desde ese equipo:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1
```

Si falla la instalación, consultar los logs y verificar Python 3.12. `requirements.txt` fija las dependencias directas; no actualizar versiones durante la presentación. No publicar logs que contengan credenciales.

## Proteger la cuota de la presentación

- **Acceso privado:** protección principal frente a personas que encuentren el enlace. Ocultar la URL no basta: una app pública puede ser indexada.
- **Separar pruebas y demo:** para reservar cuota, usar un proyecto de Google dedicado a la presentación y otro para desarrollo, sujetos a sus límites y condiciones. Otra clave del mismo proyecto **comparte la cuota**. Comprobar los modelos gratuitos disponibles en cada proyecto; no activar facturación para este MVP.
- **Modelo inicial:** se propone 3.5 Flash-Lite por la cuota comprobada por el alumno. Los otros cuatro son alternativas manuales, sin prometer disponibilidad ni cuotas independientes.
- **Antes de presentar:** verificar acceso y una conversación; evitar evaluaciones masivas ese día. Tener la web local preparada y las cinco salidas reales del notebook como respaldo identificado, sin presentarlas como respuestas en vivo.

Esto limita consumo ajeno, pero no evita saturaciones de Google ni garantiza una respuesta en tiempo real. Los errores 429/503 permiten reenviar y el cambio de modelo conserva el contexto.

## Referencias oficiales

- [Despliegue y versión de Python](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy).
- [Secretos de Streamlit](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management).
- [Apps privadas y permisos](https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app).
- [Cuotas de Gemini por proyecto](https://ai.google.dev/gemini-api/docs/rate-limits).
