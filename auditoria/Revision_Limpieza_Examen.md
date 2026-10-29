# Revisión de limpieza y organización del examen de Inteligencia Artificial

Fecha: 28 de octubre de 2026, America/Lima.

## 1. Alcance y dictamen

El notebook tiene controles adecuados de integridad relacional y de separación por conglomerados. Sin embargo, la evidencia actual no permite declarar terminada la limpieza ni asegurar el cumplimiento completo del criterio de ingeniería de datos de la rúbrica. Requieren revisión la normalización general de ausentes y categorías, la definición metodológica del rezago, los valores económicos extremos, la agregación por área y el uso del factor de expansión.

Esta revisión se basa en el código y las salidas ya guardadas de `AnalisisExamen.ipynb`, en la documentación local y en una lectura de encabezados y muestras mínimas de los CSV procesados existentes. No se ejecutaron celdas del notebook, entrenamientos, nuevas métricas predictivas, extracción de ENAHO ni lecturas completas de los CSV originales de varios gigabytes. Los resultados citados son los que ya estaban guardados; no constituyen una reproducción independiente.

Todas las correcciones que aparecen a continuación son propuestas pendientes de autorización. No se aplicó ninguna al código ni a los datos.

## 2. Protección y organización realizada

Archivos de trabajo:

- Original conservado: `AnalisisExamen.ipynb`.
- Copia de seguridad: `AnalisisExamen_BACKUP.ipynb`, creada antes de organizar el notebook.
- Copia organizada: `AnalisisExamen_Ordenado.ipynb`.
- Informe separado: `Revision_Limpieza_Examen.md`.

El original y el respaldo tienen el mismo SHA-256:

`fdc21bd5fd944162927489fe7b209f4d7ec96382cb22950e6f55b084bf4b4634`

La organización de la copia contiene ocho secciones:

1. Identificación y lectura de fuentes.
2. Inspección y EDA inicial.
3. Limpieza y validación de datos.
4. Integración ENAHO y ESCALE.
5. Construcción de variables educativas y rezago escolar.
6. Preparación de datos para Machine Learning.
7. Separación por conglomerados.
8. Validación cruzada y Regresión Logística normal/balanceada.

Se ajustaron exclusivamente encabezados Markdown y se trasladó la celda Markdown de persistencia, originalmente en la posición 45, a la posición 30, inmediatamente después del cruce y guardado preliminar. Su explicación se conserva literalmente. No se añadieron conclusiones ni correcciones dentro del notebook.

Las 46 celdas se conservaron: 26 de código, de las cuales 24 contienen instrucciones, y 20 Markdown. Todas las celdas de código mantienen exactamente su contenido, comentarios, metadatos, identificadores y orden relativo. Las 102 salidas guardadas se conservaron sin modificación. El archivo original no contiene salidas gráficas con MIME `image/*`; las tablas y demás representaciones guardadas sí se conservaron.

Las referencias de celdas en este informe utilizan posiciones del ORIGINAL, empezando en 1. Los números de ejecución guardados se incluyen cuando ayudan a identificar el bloque. La sección original 4.3 corresponde ahora a la sección 8.1. La numeración dentro de comentarios Python se dejó intacta por la condición de no modificar código.

## 3. Evidencia de los resultados existentes

| Etapa | Evidencia guardada | Alcance de la evidencia |
|---|---|---|
| Selección de 2025 | Vivienda: 44 599; Personas: 115 145; Educación: 106 958; Sumaria: 33 702 | Conteos guardados de la extracción; no se volvió a extraer |
| Edad escolar | 24 195 personas de 6 a 17 años | Población inicial del maestro |
| Personas + Educación | 23 668 coincidencias y 527 sin correspondencia | No se multiplican filas; falta explicar parte de la cobertura |
| Vivienda y Sumaria | 24 195 coincidencias en cada unión | Cobertura completa dentro de esta población seleccionada |
| ESCALE | 24 195 coincidencias | Cobertura distrital completa en el maestro guardado |
| Clasificación | 19 490 registros; 18 638 sin rezago y 852 con rezago | Definición operativa existente, todavía sujeta a justificación metodológica |
| Exclusiones | 4 705 registros | Se conserva la auditoría de motivos; no se recuperaron ni imputaron objetivos |
| Entrenamiento/prueba | 15 610 / 3 880; 0 conglomerados compartidos | Verificación guardada de `GroupShuffleSplit` |
| Validación cruzada | Tres folds, con 222, 261 y 218 positivos en validación | Folds construidos únicamente sobre entrenamiento |

Resultados de validación cruzada ya presentes:

| Modelo | F1 macro | F1 rezago | Recall rezago | Average Precision | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Regresión Logística normal | 0.4885 | 0.0000 | 0.0000 | 0.0874 | 0.6351 |
| Regresión Logística balanceada | 0.4405 | 0.1166 | 0.5461 | 0.0886 | 0.6340 |

Son promedios de validación cruzada, no resultados del conjunto final de prueba. El modelo normal no detecta positivos en las evaluaciones guardadas, según su recall de rezago igual a cero. El balanceado mejora ese recall, con el intercambio de desempeño que muestran las otras métricas. Esto es una limitación del resultado actual, no una prueba de error en las uniones ni una autorización para cambiar el modelo.

## 4. Auditoría por requisito

### 4.1. Conservación de ceros e identificadores — Correcto con límites de validación

**Evidencia:** celdas 10, 12 y 14, y muestras guardadas de las uniones. Las lecturas usan `dtype=str` o `dtype="string"`; las llaves se limpian con `str.strip()` sin convertirlas a números. Se observan códigos como `015001`, `041`, `03` y `010101`. Las muestras mínimas de los CSV procesados también conservan ceros. Los DBF definen sus códigos como campos de caracteres.

**Pendiente:** no existe una comprobación exhaustiva guardada de longitud, contenido exclusivamente numérico y pertenencia a un catálogo válido para cada identificador. `zfill(6)` en CODGEO/UBIGEO homogeneiza longitudes, pero no certifica códigos válidos y puede convertir una cadena vacía en `000000` si no se trata antes como ausente.

**Importancia:** media. Un código de seis dígitos puede seguir siendo inválido.

**Corrección propuesta:** validar ausentes antes del relleno, documentar longitudes oficiales y verificar formato y catálogo geográfico. Conservar los códigos originales como texto. No volver a convertirlos desde números.

### 4.2. Espacios, nulos y categorías especiales — Tratamiento parcial

**Evidencia:** las primeras lecturas declaran algunas cadenas de espacios como ausentes; las llaves y las categorías usadas por el modelo se normalizan con `str.strip()`. La función `a_numero` convierte blancos a ausentes antes de las comparaciones educativas. En la celda 35 todavía aparece una categoría en blanco de P308C con 13 552 registros; eso demuestra que la recuperación de variables extra no normaliza globalmente sus valores antes de mostrar distribuciones. La transformación numérica posterior sí los convierte a ausentes para el objetivo.

**Problema:** los listados de `na_values` tienen longitudes finitas de espacios y no son uniformes. Parte de la normalización se hace únicamente en series de diagnóstico, sin cambiar el maestro. Un blanco estructural por salto de cuestionario no equivale a una respuesta desconocida. La imputación de moda/mediana no documenta esa distinción.

**Importancia:** alta para la interpretación y la limpieza; no demuestra por sí sola que el entrenamiento haya fallado.

**Corrección propuesta:** acordar una regla única de blancos y un mapa por variable para códigos válidos, saltos, desconocidos y valores inválidos. No tratar automáticamente `0` como ausente: el diccionario etiqueta `0` como "pase" en P1121 y P1144, y P308B tiene ceros estructurales en primaria. Mantener separados los saltos educativos y los datos realmente faltantes. Si se aprueba una imputación aprendida de los datos, ajustarla dentro del Pipeline de cada fold.

### 4.3. Duplicados y consistencia de las uniones — Evidencia favorable

**Evidencia:** celdas 15, 18, 20, 22, 29 y 35. Los cuatro módulos reducidos muestran cero filas duplicadas, cero llaves incompletas y cero llaves repetidas en el diagnóstico guardado. Las uniones aplican `validate="one_to_one"` o `validate="many_to_one"`, indicadores de correspondencia y comprobaciones de cantidad de filas. Los UBIGEO comparables no presentan discrepancias; Educación tiene 527 casos sin comparación.

**Pendiente:** explicar los 527 escolares sin correspondencia educativa; no convertir esa ausencia en "no matriculado" ni en ausencia de rezago. La cardinalidad evita multiplicaciones, pero no prueba por sí sola la validez semántica de todos los códigos. En ESCALE no hay una salida específica de duplicados por identificador de servicio y anexo antes de sumar alumnos/docentes.

**Importancia:** media. Una repetición del servicio podría sesgar totales aunque el agregado final tenga una fila por distrito.

**Corrección propuesta:** conservar el reporte de cobertura y comprobar la unidad de registro de ESCALE, incluyendo COD_MOD y ANEXO cuando corresponda. No eliminar anexos ni deduplicar por COD_MOD sin justificar la unidad oficial.

### 4.4. P306, P307, P308A, P308B y P308C — Distinción principal correcta; documentación por precisar

**Evidencia documental:** cuestionario ENAHO01A 2025, página 2; diccionario panel, páginas PDF 589, 590 y 662.

| Variable | Interpretación respaldada | Uso actual |
|---|---|---|
| P306 | Matrícula en el año de la encuesta; 1: sí, 2: no | Se exige `P306_25 == "1"` para construir el objetivo |
| P307 | Asistencia actual en el cuestionario; 1: sí, 2: no | Se inspecciona, pero no se exige asistencia para clasificar |
| P308A | Nivel en el que está matriculado; 2: primaria, 3: secundaria | Selecciona los dos niveles de análisis |
| P308B | Año de estudios | Se usa para secundaria, años 1 a 5 |
| P308C | Grado de estudios | Se recupera y usa para primaria, grados 1 a 6 |

**Hallazgo favorable:** la construcción final distingue el año de secundaria del grado de primaria. En la auditoría previa, el comentario de P308B como "Grado educativo" es impreciso; la recuperación de P308C corrige el uso efectivo posterior. No se cambió ese comentario.

**Inconsistencia de la documentación:** la etiqueta de P307 del diccionario panel, página PDF 589, menciona educación a distancia; el cuestionario 2025, página 2, formula asistencia general. Por ello no corresponde certificar una interpretación más específica sin aclarar esta discrepancia. El código actual no utiliza P307 como predictor ni como condición del objetivo.

**Pendiente:** justificar que la población del objetivo sean matriculados, incluyendo quienes actualmente no asisten. No exigir P307=1 automáticamente: eso cambiaría la población. También debe comprobarse el alcance de educación básica alternativa, ya que no se seleccionó P307D y los códigos de nivel no bastan para asegurar que toda la muestra sea EBR.

**Corrección propuesta:** documentar el universo elegido y el significado de cada variable con sus fuentes; aclarar P307 y el alcance EBR/CEBA antes de cambiar filtros.

### 4.5. REZAGO_ESCOLAR — Implementación coherente con su definición; justificación pendiente

**Evidencia:** celda 36, ejecución guardada 23. Se exigen matrícula, edad entre 6 y 17, primaria con grado válido o secundaria con año válido. Se calcula edad normativa como grado + 5 en primaria y año + 11 en secundaria. El objetivo vale 1 cuando edad >= edad normativa + 2. La tabla guardada muestra edades normativas de 6 a 11 en primaria y de 12 a 16 en secundaria, sin combinaciones incoherentes en esa salida.

**Problema metodológico:** el umbral de dos años es una decisión operativa que debe sustentarse. La guía describe superar la edad normativa, sin fijar explícitamente dos años en ese pasaje. La edad al momento de la entrevista y el calendario escolar pueden afectar la clasificación; no se ha comprobado aquí una definición oficial con su fecha de referencia.

**Importancia:** alta. Una definición alternativa cambiaría etiquetas, población y resultados.

**Corrección propuesta:** validar con el criterio de evaluación o una fuente metodológica pertinente el umbral y la fecha de referencia; documentar la decisión antes de regenerar etiquetas. No imputar grado o rezago para recuperar casos sin información. Mantener la exclusión de los 4 705 casos explicada por motivo.

**Fuga directa:** en la selección actual de predictores no aparecen edad, grado, edad normativa, nivel escolar ni el propio objetivo; se evita utilizar directamente los componentes deterministas de la etiqueta como variables explicativas. Esto no reemplaza las demás comprobaciones de fuga.

### 4.6. Variables socioeconómicas y extremos — Insuficientemente validado

**Evidencia:** pobreza, ingreso, gasto y FACTOR07 se incorporan desde Sumaria con cobertura completa para los escolares. POBREZA muestra códigos 1, 2 y 3 en las salidas. INGHOG2D y GASHOG2D se convierten a números al preparar X.

**Pendiente:** no se guardan diagnósticos suficientes de distribución, cuantiles, valores no finitos, conversiones fallidas o extremos de ingresos/gastos. `errors="coerce"` puede convertir valores no interpretables a ausentes sin informar cuántos. `StandardScaler` no elimina valores extremos; la mediana imputa ausentes, pero no valida montos.

La documentación de Sumaria identifica ingresos y gastos totales anuales del hogar. No se construyen importes per cápita; la guía menciona esa construcción y no se selecciona MIEPERHO en la configuración inicial. Tampoco se seleccionan P204/P205/P206 para comprobar la condición de miembro/residencia de la población antes de realizar inferencia poblacional.

**Importancia:** alta para interpretar la situación económica y evaluar la limpieza.

**Corrección propuesta:** verificar unidades, universo, distribuciones y valores inválidos; justificar cualquier tratamiento de extremos. No suprimir automáticamente ingresos netos negativos, que deben interpretarse según su definición. Si se aprueban variables per cápita, obtener y validar el denominador correcto; si se aprueban transformaciones aprendidas o límites por cuantiles, ajustarlos dentro de entrenamiento/folds. No se realizó ninguna de estas operaciones.

### 4.7. ESCALE y ratio alumnos/docente — Mejora aplicada en el trabajo original, con pendientes

**Evidencia:** celdas 27, 32 y 40. Los campos reales son TALUM, TDOC y TSEC. El indicador usa suma de alumnos / suma de docentes y evita dividir por cero. La auditoría inicial identifica 17 668 servicios con alumnos y TDOC=0, correspondientes a la frecuencia guardada del programa inicial no escolarizado; esa igualdad de conteos orienta la revisión, sin sustituir una comprobación registro por registro.

La corrección ya existente restringe el nuevo ratio a Primaria y Secundaria. El modelo usa `ratio_docente_ps`; no usa el ratio inicial de todas las modalidades seleccionadas. La salida de ese nuevo indicador tiene 19 490 valores presentes, mínimo 2.089552 y máximo 23.335780. La unión valida muchos-a-uno y no multiplica registros.

**Pendientes:**

- La guía propone agregación por distrito y área urbana/rural. El código agrupa solo por CODGEO. DAREACENSO se lee, pero no entra en el `groupby`; ESTRATO se conserva en el maestro, pero no se utiliza para enlazar por área ni como predictor actual.
- El ratio corregido cubre Primaria/Secundaria, mientras `proporcion_publicos` procede de la agregación que también incluye inicial y `locales_escolares` cuenta locales activos sin el mismo filtro de niveles. Es una diferencia de universo que debe declararse o armonizarse, no un error aritmético demostrado.
- No se conservan en la selección de campos ANEXO, IMPUTADO y DES_IMPUTA para auditar anexos y procedencia/imputación de los totales. Las sumas pueden ocultar faltantes si no se acompaña la cobertura de componentes.
- Las coordenadas se filtran por rangos generales y se promedian por registros de servicio. No se ha validado su precisión, su ubicación distrital ni un posible mayor peso de locales con varios servicios.

**Importancia:** alta para alinearse con la agregación solicitada y media para la interpretación contextual.

**Corrección propuesta:** acordar y documentar distrito/área y universo escolar; verificar la unidad del padrón y la calidad de conteos antes de nuevas agregaciones. Conservar la distinción entre indicador contextual distrital y escuela individual a la que asiste cada estudiante.

### 4.8. Fuga de datos, separación y Pipeline — Evidencia favorable al alcance revisado

**Evidencia:** celdas 42 y 44. `GroupShuffleSplit(test_size=0.20, random_state=42)` separa por CONGLOME. La salida confirma 0 grupos compartidos. `GroupKFold(n_splits=3)` se construye sobre entrenamiento; cada fold incluye una aserción de disjunción y los mismos folds se reutilizan para ambas configuraciones.

Imputación numérica por mediana, escalado, imputación categórica por moda y One-Hot están dentro del Pipeline pasado a `cross_validate`. Esas operaciones se ajustan dentro de cada fold. Las conversiones deterministas de tipos y espacios previas al split no estiman estadísticas poblacionales. Las agregaciones de ESCALE utilizan una fuente contextual y no el objetivo de ENAHO.

**Límites:** no se ejecutó una auditoría dinámica independiente. Separar conglomerados no obliga a separar distritos: un mismo distrito puede aparecer en entrenamiento y prueba. Por tanto, no debe afirmarse generalización a distritos totalmente nuevos ni ausencia absoluta de toda dependencia espacial. El test final sigue reservado según el código y las salidas actuales; esta revisión no utiliza sus resultados para elegir modelos.

**Corrección propuesta:** mantener el esquema solicitado por conglomerado y expresar con precisión el alcance de generalización. Cualquier ajuste futuro de transformaciones o selección de variables debe realizarse usando entrenamiento y validación, sin consultar el test final.

### 4.9. FACTOR07 y ponderación — Conservado, pero no utilizado

**Evidencia:** FACTOR07_25 está en la extracción de Sumaria y en el maestro. No se utiliza para ponderar ajuste, métricas ni descripción de resultados en el bloque de modelado. `class_weight="balanced"` corrige la contribución relativa de las clases en el clasificador; no equivale al factor de expansión muestral.

**Importancia:** alta. La guía solicita considerar el factor de expansión; conservar una columna no demuestra esa consideración metodológica.

**Corrección propuesta:** definir y documentar si el análisis es muestral o poblacional, comprobar el peso apropiado para la unidad persona/hogar y decidir dónde ponderar. El diccionario también documenta FACPOB07 para población, que no se seleccionó en los CSV reducidos. No corresponde sustituir un factor por otro sin verificar universo y metodología. Si se autoriza ponderar, comprobar por separado su aplicación compatible en el ajuste y en las métricas. No usar el peso como predictor solo para aparentar cumplimiento.

### 4.10. Panel 2021–2025 frente a anual 2025 — Reconocido, equivalencia no demostrada

**Evidencia:** el Markdown original ya advierte la diferencia. La extracción conserva columnas `_25` y filtra AÑO_25=2025. La ficha técnica indica que los archivos contienen hogares panel y no panel de cada año; el nombre PANEL no significa que todos los registros sean exclusivamente del panel común de cinco años.

**Pendiente:** no se contrastó la selección completa con la base anual independiente de 2025 ni sus filtros, factores y universo. La muestra panel de 12 096 viviendas que menciona la ficha no es el tamaño total que debe atribuirse a todos los registros `_25` del archivo. Seleccionar indicadores HPAN/PERPANEL para exigir presencia en todos los años cambiaría el universo y no forma parte del código actual.

**Importancia:** alta para inferencia y presentación del diseño del estudio.

**Corrección propuesta:** describir con exactitud "corte 2025 extraído del archivo panel 2021–2025" y comprobar su correspondencia con la muestra anual antes de afirmar equivalencia. Aplicar factores longitudinales solo si el diseño elegido requiere efectivamente un panel longitudinal.

## 5. Reproducibilidad, persistencia y alcance del archivo

### 5.1. Dependencias comprobadas de forma estática

Se compararon todas las celdas de código del original y de la copia organizada, incluyendo su orden relativo: son idénticas. Por ello, la organización no adelanta consumidores de variables respecto de sus definiciones originales. La cadena principal conserva configuración -> extracción/lectura -> personas escolares -> integración ENAHO -> ESCALE -> maestro -> grado -> clasificación -> ratio corregido -> partición -> validación logística.

Se analizó sintaxis Python de 25 celdas, incluidas las dos vacías. La celda restante es la instrucción IPython `%pip install dbfread`, conservada literalmente; no se ejecutó ni se trató como Python ordinario. Se verificó que el archivo organizado puede volver a leerse como JSON y conserva la estructura de notebook 4.5. No se ejecutó un kernel ni se certificó compatibilidad dinámica de todas las bibliotecas.

### 5.2. Bloqueo existente en una ejecución desde cero

**Evidencia:** celda 12, ejecución guardada 5. La extracción lanza `FileExistsError` si encuentra un CSV reducido ya creado. Los cuatro destinos existen actualmente. Por tanto, ejecutar todas las celdas desde un kernel nuevo con el directorio actual se detendría en esa protección, antes del resto del análisis.

**Corrección propuesta:** acordar un flujo explícito para reutilizar las extracciones existentes, sin sobrescribirlas, o un modo de extracción separado y controlado. Requeriría modificar código o instrucciones de ejecución y no se implementó. El código conserva rutas absolutas de Windows, de modo que su ejecución directa en Colab también necesitaría adaptación autorizada de acceso y rutas. Esta copia organizada no se declara completamente reproducible ni lista para ejecutarse sin ajustes en Colab.

### 5.3. Persistencia descrita y persistencia real

El Markdown de persistencia dice que se generan dos datasets. En el código existente solo se guarda el maestro preliminar de 24 195 personas. El archivo `dataset_integrado_preliminar_2025.csv` tiene las 50 columnas previas a recuperar P308C/P308D y a calcular REZAGO_ESCOLAR y `ratio_docente_ps`. No se encontró un CSV persistido de clasificación entre los archivos actuales de `data/processed`.

La celda de código final está vacía. Por ello, no se puede afirmar que el dataset final de clasificación esté guardado. Además, el guardado preliminar no sobrescribe un archivo ya existente; la coincidencia entre ese archivo y un estado futuro de memoria tendría que comprobarse explícitamente.

**Corrección propuesta:** cuando se autorice, alinear la descripción de persistencia con lo realmente guardado y definir una exportación versionada del dataset de clasificación. No se creó, alteró ni reemplazó ningún CSV en esta revisión.

### 5.4. Secciones posteriores, diagnósticos y posibles retiradas

Después de la sección original 4.3 solo había un Markdown de persistencia y una celda vacía. No hay bloques implementados posteriores de Random Forest, XGBoost, LightGBM, clustering o SHAP. El Markdown se conservó y reubicó; la celda vacía se conservó.

No hay salidas de tipo `error` guardadas en el archivo recibido. Esto no demuestra que nunca hubiera errores en sesiones anteriores. Los contadores de ejecución tienen saltos y no sustituyen una ejecución completa y verificable.

Posibles simplificaciones futuras, TODAS pendientes de autorización:

- Celdas vacías 1 y 46: podrían retirarse por presentación.
- Celda 34, diagnóstico del encabezado/separador: podría compactarse cuando quede documentada la recuperación correcta del grado; hoy aporta trazabilidad.
- Celda 24, instalación de dbfread: podría trasladarse a una sección explícita de entorno si se acuerda un esquema de ejecución.
- Inventarios, muestras, auditorías de exclusiones y el ratio inicial: conservarlos como evidencia o moverlos a un anexo si se autoriza; no descartarlos automáticamente.

Ninguna celda se eliminó, ni se consolidaron importaciones o comentarios repetidos.

## 6. Relación con la rúbrica y pendientes priorizados

| Prioridad | Pendiente | Consecuencia para la evaluación | Propuesta, sin aplicar |
|---|---|---|---|
| Alta | Sustento del umbral y universo de REZAGO_ESCOLAR | La etiqueta determina todo el problema supervisado | Confirmar criterio y documentar matrícula/asistencia, calendario y alcance EBR |
| Alta | Consideración efectiva del factor de expansión | La guía lo menciona y el código actual no lo usa | Definir unidad, ponderación y justificación metodológica |
| Alta | Ausentes estructurales y códigos especiales | Una imputación genérica puede mezclar significados | Validación por variable y saltos del cuestionario |
| Alta | Distribuciones económicas y extremos no auditados | No se puede certificar limpieza suficiente | Diagnosticar unidades y valores antes de decidir tratamientos |
| Alta | Agregación ESCALE solo por distrito | Difiere de distrito/área descrito en la guía | Justificar o armonizar geografía y universo de indicadores |
| Media | Universo del corte 2025 y residentes | Limita afirmaciones de representatividad | Contrastar documentación y muestra anual antes de inferir |
| Media | Persistencia incompleta de clasificación | Falta evidencia de exportación del dataset de modelado | Exportación futura autorizada y versionada |
| Media | Ejecución completa bloqueada por archivos existentes | La organización no basta para asegurar reproducibilidad | Acordar reutilización segura de archivos procesados |

La revisión respalda los controles relacionales y el esquema de prevención de fuga observados. No asigna una nota ni certifica que los datos estén "totalmente limpios". Tampoco considera un defecto de esta intervención que todavía falten modelos avanzados, clustering, SHAP o evaluación final: el alcance autorizado termina en la regresión logística mediante GroupKFold. Esas partes de la rúbrica quedan fuera de esta etapa y no se desarrollaron.

Para incorporar conectividad, computadoras e infraestructura escolar detallada siguen faltando las tablas de datos correspondientes; los diccionarios disponibles no las reemplazan. Los dos ZIP inválidos de matrícula/docentes no se usan en el pipeline existente y los totales básicos utilizados provienen del padrón válido. No se descargaron nuevas bases.

## 7. Fuentes locales y trazabilidad

- [Notebook original](<D:/Proyectos Grandes Curos 2026-2/Examen de Inteligencia Artificial/AnalisisExamen.ipynb>): código, comentarios, salidas y metadatos. Las referencias a posiciones de celda de este informe apuntan a este archivo.
- [Guía del examen](<D:/Proyectos Grandes Curos 2026-2/Examen de Inteligencia Artificial/guía de evaluación - proyecto ia_ brecha digital y educación 2025 (enaho - escale)_r82irt6hai (2).pdf>): páginas PDF 2–7; fuentes, agregación distrital/área, prevención de fuga, variables, ponderación y rúbrica.
- [Ficha técnica panel](<D:/Proyectos Grandes Curos 2026-2/Examen de Inteligencia Artificial/ENAHO-20261027T204051Z-1-001/ENAHO/INEI/1041-Ficha.pdf>): páginas PDF 2–7; muestra panel, inferencia, universos y selección de paneles. En la revisión previa se comprobó que las copias de las seis carpetas de módulos son idénticas a esta ficha.
- [Diccionario panel 2021–2025](<D:/Proyectos Grandes Curos 2026-2/Examen de Inteligencia Artificial/ENAHO-20261027T204051Z-1-001/ENAHO/INEI/1041-Modulo1475/1041-Modulo1475/Diccionario_panel_2021_2025.pdf>): páginas PDF 588–590, 599, 653, 657, 658 y 662; variables educativas, factores, montos y códigos. Las páginas mencionadas son la numeración física del PDF.
- [Cuestionario ENAHO01A 2025](<D:/Proyectos Grandes Curos 2026-2/Examen de Inteligencia Artificial/ENAHO-20261027T204051Z-1-001/ENAHO/INEI/1041-Modulo1475/1041-Modulo1475/CUESTIONARIO_ENAHO01A_2025.pdf>): página PDF 2; matrícula, asistencia, niveles, año/grado y CEBA.
- [Documentación de Sumaria](<D:/Proyectos Grandes Curos 2026-2/Examen de Inteligencia Artificial/ENAHO-20261027T204051Z-1-001/ENAHO/INEI/1041-Modulo1478/1041-Modulo1478/21_Sumaria_PANEL_2021-2025.pdf>): páginas PDF 120–125; ingresos/gastos anuales, miembros del hogar y factor anual.
- Encabezados y muestras mínimas de los cinco CSV ya existentes en `data/processed`: comprobación de nombres, columnas persistidas y ejemplos de identificadores. No se calcularon nuevas métricas predictivas ni se reejecutó la limpieza.

## 8. Verificaciones de conservación

- Original y respaldo: igualdad de contenido y SHA-256.
- Código y orden relativo: igualdad exacta de las 26 celdas de código.
- Explicaciones: igualdad de todas las líneas no vacías ajenas a encabezados Markdown.
- Salidas: igualdad exacta de las 102 salidas guardadas, asociadas a sus mismas celdas.
- Identificadores, metadatos y contadores de ejecución: conservados.
- Celdas útiles, diagnósticos y celdas vacías: conservados.
- Sintaxis: revisión estática sin ejecución.
- Datasets: ninguna modificación autorizada ni realizada; no se regeneraron CSV ni DBF.

Las propuestas de este informe quedan pendientes. El notebook organizado conserva tanto los aciertos como las limitaciones metodológicas del trabajo original.
