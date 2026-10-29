# Informe final de entrega y auditoría contra la guía

Fecha: 28 de octubre de 2026. Estado vigente de la entrega. Los informes `Auditoria_Final_Reproducibilidad.md` y `Revision_Limpieza_Examen.md` conservan el registro histórico anterior; sus afirmaciones de que no se ejecutó Run All quedaron superadas por la prueba documentada aquí.

## Productos comprobados

- Artículo IEEE A4 derivado de plantilla de conferencia IEEE auténtica, Word editable y PDF de seis páginas. Nueve figuras y ocho tablas; sin bloques de autoría por instrucción del estudiante. Bibliografía verificable y texto científico definitivo, sin comentarios editoriales ni instrucciones de la plantilla.
- Notebook final de 118 celdas, construido sobre la copia de 116: dos celdas adicionales resuelven rutas portables y documentan el alcance de los extractos.
- Dataset principal de 19 490 filas y 58 columnas; extensión por área de 19 490 filas; diccionario de 78 variables con ubicación y semántica.
- Cuatro extractos de módulos ENAHO, dos cachés ENAHO adicionales y los dos ZIP ESCALE necesarios; no se distribuyen microdatos gigantes ni ZIP inválidos.
- Modelo, figuras originales, figuras compactas del artículo, tablas de referencia y reproducidas, complementos ponderados y geográficos, código, README, dependencias y hashes.

## Reproducción efectivamente ejecutada

`ejecucion_kernel_limpio.json`: éxito, 118 celdas, 103,18 segundos, kernel nuevo, sin errores. Se ejecutaron secuencialmente todas las celdas de la copia portable con los extractos distribuidos. No hubo variables residuales. Se entrenaron realmente las diez configuraciones supervisadas, K-Means y GMM iniciales y refinados con k de 2 a 6, los candidatos de perfilado y el XGBoost final. Se recalcularon evaluación final, calibración y SHAP.

Se compararon las cinco tablas de referencia: clasificación, clustering refinado, perfiles, métricas de prueba y matriz de confusión. No hubo diferencias numéricas en los valores persistidos; la tolerancia admitida fue 0,00005 y el máximo observado fue cero. Las tablas comparativas originales tienen redondeo de cuatro decimales; esta coincidencia no demuestra identidad de todas las matrices internas ni igualdad bit a bit de cada modelo serializado.

Se ejecutó adicionalmente una sensibilidad XGBoost 2×2 con tres GroupKFold (12 ajustes), exclusivamente en entrenamiento. Se conservaron el criterio y el ganador histórico; no se evaluó el complemento sobre prueba. Se exportaron las tablas FACPOB07 y área desde los mismos bloques del notebook. Se reconstruyó el K-Means k=2 para la figura compacta y se verificaron tamaños [8310,7300], silueta 0,26811408 y PCA 0,63760960.

## Evidencias por criterio de la rúbrica de 20 puntos

| Criterio | Máximo | Evidencias presentes | Alcance o límite |
|---|---:|---|---|
| Ingeniería y prevención de fuga | 5 | Llaves textuales completas, control de cardinalidad y duplicados, GroupShuffleSplit, tres GroupKFold, asserts sin intersección, pipelines dentro de cada entrenamiento | Contexto histórico por distrito; el cruce por área está separado. No es validación por distritos inéditos ni temporal |
| Clustering | 4 | K-Means y GMM k=2–6, escalado, refinamiento, silueta, DB, CH, PCA, silueta gráfica, tabla y nombres de perfiles | Silueta moderada; desfase incluido. Recursos del hogar totales, no per cápita. No prueba una tipología integral de brecha digital |
| Clasificación | 5 | Baseline y tres arquitecturas avanzadas, diez configuraciones, balanceo, CV agrupada, sensibilidad acotada de hiperparámetros, métricas y curvas finales | No búsqueda exhaustiva ni anidada; F1 positivo bajo y calibración insuficiente. No nueva selección en prueba |
| SHAP | 3 | Beeswarm de diez características más fila agrupada, dos dependencias, dos Waterfall, interpretación global/local y límites | 300 filas de entrenamiento; dummies como características; asociaciones predictivas sin causalidad |
| Artículo, orden y defensa | 3 | Artículo de seis páginas IEEE, README, carpeta estructurada, código fuente, diccionario, evidencia de ejecución, PDF y ZIP | La defensa oral no puede certificarse mediante archivos; la calificación corresponde al docente |

La tabla acredita presencia y alcance de evidencias; no asigna ni garantiza una calificación. Los ejemplos de variables de la guía no deben confundirse con mediciones disponibles: no se inventaron altitud, competencias digitales ni conectividad escolar.

## Observaciones metodológicas que permanecen

1. Se utilizó corte `_25` del panel 2021–2025. No quedó demostrada la equivalencia completa con la base anual independiente mencionada por la guía.
2. Edad a entrevista frente a edad al 31 de marzo; EBR/CEBA no completamente aisladas. Las etiquetas no se cambiaron silenciosamente.
3. P1121/P1144 conservan los códigos originales de pase, sin convertirlos universalmente a negativos confirmados.
4. Predictores históricos agregados por distrito. El complemento por distrito y área se entrega con 377 observaciones sin enlace, sin sustitución por agregados más amplios.
5. FACTOR07 y FACPOB07 tienen propósitos distintos. FACPOB07 pondera la descripción de residentes de entrenamiento; el clasificador y sus métricas son no ponderados. No hay inferencia nacional con diseño complejo.
6. Se preserva la baja precisión positiva 0,064806 y el Brier 0,188955. No se corrigieron métricas ni se recomienda una implementación automática.
7. La reproducción certificada parte de extractos y cachés incluidos. La extracción completa desde CSV panel de varios gigabytes se suministra como código, pero no se ejecutó de nuevo para los cuatro módulos. Colab y otros sistemas operativos no fueron el entorno certificado.

## Formato y revisión documental

Se conservaron estilos, tema, fuentes y numeración de la plantilla IEEE A4. Se eliminaron las instrucciones, ejemplos y secciones de tres columnas para autores por petición explícita de omitir autoría. Se mantuvieron título y cuerpo a dos columnas; no se redujeron márgenes ni fuente de cuerpo para alcanzar el límite de páginas. Las figuras se recompusieron para mejorar la lectura.

`render_docx.py` se intentó sobre el artículo final y falló por ausencia de `soffice.exe` (LibreOffice). Se resolvió exportando el DOCX con Microsoft Word instalado y rasterizando el PDF con Poppler. Se abrieron y revisaron las seis páginas como imágenes; el PDF final tiene seis páginas A4. Esta sustitución del motor es una limitación del entorno, no del documento entregado.

## Conservación y cierre

Los originales, sus respaldos, CSV, DBF, modelos, tablas y figuras del proyecto principal se contrastan con un manifiesto previo de tamaño, fecha y SHA-256 cuando estaba disponible. Los resultados de la comparación están en `conservacion_originales.json`. El manifiesto final permite comprobar los archivos entregados. El ZIP se valida con CRC, tamaños y SHA-256 de cada entrada, y se prueba desde una extracción independiente. Los resultados de esa comprobación se documentan en `validacion_zip.json` y `prueba_portabilidad_zip.json`.

## Prueba final desde el ZIP extraído

Se extrajo el ZIP de prueba en una carpeta independiente y se verificaron los 127 archivos de su manifiesto. Sin DBF intermedios previos, el notebook volvió a extraer ESCALE desde los ZIP incluidos. El ejecutor distribuido creó un kernel nuevo y completó las 118 celdas en 98,10 segundos, sin errores. Las cinco tablas principales coincidieron exactamente con las referencias. Esta segunda prueba confirma la portabilidad de los datos y las rutas del paquete, además de la primera ejecución de 103,18 segundos.
