# Auditoría final de reproducibilidad y conservación

Fecha: 28 de octubre de 2026, America/Lima.

## 1. Resultado y alcance

Se creó `AnalisisExamen_Final_Ordenado.ipynb` a partir del original completo de 97 celdas.
La copia final contiene 116 celdas. Conserva las 97 originales, sus identificadores,
sus 251 salidas y sus 17 salidas gráficas, sin reemplazarlas por métricas nuevas. Los
textos explicativos originales se conservan; se renumeraron encabezados y se añadieron
celdas metodológicas e interpretativas autorizadas.

Se corrigieron los bloqueos identificados para reutilizar CSV y se recuperó la preparación
original de clustering. La validación fue selectiva: NO se ejecutó Run All, NO se reentrenaron
los diez clasificadores, NO se reentrenaron K-Means/GMM y NO se ajustó el modelo definitivo.
El escalado y PCA de preparación sí se comprobaron como prueba ligera, sin recalcular etiquetas.
No se preparó artículo ni ZIP.

## 2. Protección de archivos

- Respaldo adicional: `AnalisisExamen_BACKUP_Completo.ipynb`.
- SHA-256 del original y respaldo: `7e6e0a15ee0acef1cdf5178cedd25f8ac4a97248bc636ba13ca09aa7c673fd58`.
- SHA-256 del modelo original: `efd38a1d3c3a520a69c22149bf3676ec0f5ea6ce7ef6ebb786f0e31d79795d1c`.
- Las nuevas ejecuciones de la copia escriben en `resultados_final_ordenado`.
- Los CSV reducidos y maestros existentes se validan y reutilizan. No se sobrescriben.
- No se modificaron el original, los respaldos previos, los CSV/DBF, figuras, tablas ni modelo original.

La comprobación final de tamaños, fechas y hashes de los archivos anteriores se realiza también
fuera de este notebook. Este documento no afirma ejecución de rutas que solo se analizaron estáticamente.

## 3. Preparación original de clustering recuperada

Se localizó el código exacto en `.ipython/profile_default/history.sqlite`, sesión 66,
ejecución 43. Se recuperaron sus pasos 1–6: `datos_cluster = df_modelo.iloc[train_idx].copy()`,
cinco variables numéricas originales, P1121/P1144, desfase edad–edad normativa, log1p para
ingreso, gasto y locales escolares, y get_dummies con dtype=float. Se importan StandardScaler
y PCA antes de su primer uso. La celda posterior conserva la conversión float64 y el escalado
originales. No se incorporó la versión fallida del chequeo previo a esa conversión.

SHA-256 del fragmento recuperado: `78b2f3608776e79c46192ecfc13dbce19d1433457650060e36858d6416448caa`.

Verificaciones ejecutadas:

- Matriz recuperada: 15610 registros, 10 columnas y orden original.
- Columnas: `['INGHOG2D_25', 'GASHOG2D_25', 'ratio_docente_ps', 'proporcion_publicos', 'locales_escolares', 'desfase_anios', 'P1121_25_0', 'P1121_25_1', 'P1144_25_0', 'P1144_25_1']`.
- PCA inicial: 51.734938 %, que coincide al redondear con 51.73 % guardado.
- PCA refinado: 63.760960 %, que coincide al redondear con 63.76 % guardado.
- Los seis campos refinados y las cuatro dummies excluidas coinciden con las salidas anteriores.

No existe un vector de etiquetas de cada persona persistido para una comparación punto a punto.
Se preservaron código, tablas, figuras y perfiles guardados; NO se certifica identidad numérica
de etiquetas tras un entrenamiento que no se realizó. La recuperación literal y la coincidencia
de preparación aportan evidencia, pero no sustituyen esa prueba integral.

## 4. Reutilización y generación de CSV

Se añadió `validar_csv_procesado`: comprueba columnas, número de filas del corte de referencia,
unicidad y completitud de llaves, sus longitudes, formatos geográficos y años presentes.
Los blancos de Educación en el maestro por falta de correspondencia no se confunden con un año inválido.
La comprobación de estructura no exige un orden artificial diferente de columnas.

Se probaron las ramas de reutilización de los cuatro CSV reducidos existentes, y se validaron
los tres datasets integrados/preliminares ya presentes. Si falta un reducido, la copia permite
generarlo desde su fuente en bloques, con apertura exclusiva `x`, sin sustituir archivos.
La rama de generación se verificó por inspección y sintaxis; no se ejecutó sobre fuentes gigantes.
Un fallo durante una generación futura puede dejar un CSV parcial que la validación rechazará;
no se borra ni reemplaza automáticamente. Los conteos corresponden al corte fijo de esta evaluación.

No se afirmó equivalencia íntegra de los CSV con todas las celdas originales: una validación
estructural y de conteos no demuestra igualdad de cada valor. Se preservaron sus hashes.

## 5. Ponderación y universo

El diccionario panel 2025 identifica FACPOB07 como factor anual de personas y FACTOR07
en Sumaria. La descripción complementaria usa FACPOB07 sobre residentes habituales
con peso positivo y finito de la submuestra de entrenamiento; los modelos originales siguen
siendo comparaciones predictivas no ponderadas. `class_weight` y `scale_pos_weight` no se
presentan como pesos muestrales. No se utiliza un factor longitudinal de panel común.

Se leyó únicamente el módulo 200 de aproximadamente 298 MB, seleccionando nueve columnas
para el año 2025. No se releyeron los módulos de educación/salud/empleo de varios gigabytes.
Las llaves personales recuperadas se validaron y el cruce fue uno-a-uno, sin alterar df_modelo.

| Control | Registros |
| --- | --- |
| Cohorte de clasificación | 19490 |
| Residentes habituales de la cohorte | 19286 |
| Entrenamiento residente con peso personal positivo | 15448 |

| Área | Registros | Suma de pesos de la submuestra | Rezago muestral (%) | Rezago ponderado FACPOB07 (%) |
| --- | --- | --- | --- | --- |
| Total | 15448 | 4891486.4939 | 4.4731 | 4.1602 |
| Urbana | 9828 | 3876795.0069 | 3.897 | 3.889 |
| Rural | 5620 | 1014691.487 | 5.4804 | 5.1964 |

Estas tasas describen el dominio analítico del entrenamiento, no a todos los escolares del Perú.
La suma de pesos de una submuestra no es una estimación del total nacional; no hay reajuste
por partición ni intervalos con el diseño complejo. La residencia usa la fórmula documentada
por INEI, corroborada con P204/P205/P206 de la documentación 2025. La equivalencia entre el
corte `_25` del panel y la base anual independiente continúa sin demostrarse completamente.

## 6. ESCALE por distrito y área

Se construyó una versión complementaria con AREA_CENSO=1 Urbana / 2 Rural, comprobada
contra DAREACENSO. En ENAHO se mapea ESTRATO 1–5 a Urbana y 6–8 a Rural según su
diccionario. Se incluyen servicios activos de primaria B0 y secundaria F0. Se comprobó
unicidad de COD_MOD–ANEXO; se mantienen los anexos como parte de la unidad de servicio.

El agregado incluye sumas de alumnos, docentes y secciones, locales únicos, proporción de
servicios públicos y coordenadas válidas. El ratio es suma de alumnos/suma de docentes,
sin imputar denominadores cero. El cruce por distrito y área valida muchos-a-uno.

| AREA_ENAHO | Registros | Coincidencias | Ratio_disponible |
| --- | --- | --- | --- |
| Rural | 7012 | 6961 | 6961 |
| Urbana | 12478 | 12152 | 12152 |

Se obtuvieron 2439 combinaciones distrito–área
y 19490 observaciones en la versión extendida. No se
sustituyó `ratio_docente_ps`, `proporcion_publicos` ni ningún predictor de X. La cobertura
por área se informa aunque no sea completa; no se utiliza el agregado distrital como
relleno silencioso. El área de residencia no demuestra la escuela individual de matrícula.

## 7. Códigos especiales, rezago y EDA

P1121 y P1144 conservan 0 como pase y 1 como alternativa declarada. No se recodifica 0
automáticamente a negativo confirmado ni se imputa como ausencia desconocida. Las
categorías especiales de lengua materna se conservan separadas. Los diez modelos siguen
usando los códigos originales; afirmar que el complemento cambia su semántica sería incorrecto.

El umbral de dos o más años concuerda con la ficha de ESCALE, que utiliza edad al 31 de
marzo. El experimento mantiene edad a la entrevista: es una aproximación documentada y
no una reproducción exacta del indicador SIAGIE. La identidad de todas las etiquetas actuales
con edad >= edad normativa + 2 se comprobó sin regenerarlas. Se mantienen los 19 490 casos,
852 positivos y 4 705 exclusiones de la población inicial. Se conserva matrícula P306 y la
distinción P308C en primaria / P308B en secundaria. El universo EBR/CEBA no se certifica
totalmente porque P307D no se incorporó al experimento original.

Las auditorías de faltantes, convertibilidad, extremos y sensibilidad se mantienen completas.
Las seis figuras EDA originales se reubicaron después de existir df_modelo y train_idx,
antes de los modelos; sus tablas, salidas y datos de entrenamiento se conservaron.

## 8. Modelos, grupos, métricas y SHAP

Las diez configuraciones supervisadas conservan código, parámetros, semillas y salidas.
El sobremuestreo permanece dentro del entrenamiento de cada fold; los pesos positivos se
calculan con entrenamiento. No se añadió sobremuestreo a XGBoost o LightGBM.

Se reconstruyó GroupShuffleSplit y los tres folds sin entrenar clasificadores. Coinciden
15 610/3 880 registros y los conteos de folds [[10406, 5204, 222], [10407, 5203, 261], [10407, 5203, 218]]; se comprobaron intersecciones
vacías entre entrenamiento/validación/prueba a nivel CONGLOME.

Se cargó el Pipeline joblib original, sin fit. Sus predicciones reproducen los nueve valores
del CSV de métricas dentro de tolerancia rtol=1e-10, atol=1e-12 y la matriz [[2791,938],[86,65]].
Esta consulta de prueba fue una comprobación de integridad de un modelo ya seleccionado,
no selección ni ajuste posterior. No se declaró evaluado un modelo nuevo.

| Métrica | Verificado |
| --- | --- |
| Accuracy | 0.736082 |
| Precision rezago | 0.064806 |
| Recall rezago | 0.430464 |
| F1 rezago | 0.112652 |
| F1 macro | 0.478821 |
| ROC-AUC | 0.625042 |
| Average Precision | 0.092119 |
| PR-AUC | 0.089826 |
| Brier Score | 0.188955 |

Se verificó la reconstrucción SHAP del mismo modelo y las mismas 300 filas de entrenamiento.
Se conservan los casos Waterfall en posiciones de prueba [3648, 577], con probabilidades
[0.8592256307601929, 0.040169477462768555] (0.8592 y 0.0402 redondeadas). Los cinco gráficos
originales permanecen en sus celdas. Se añadió una variante global con max_display=11:
diez características individuales y una fila agrupada; el conteo de etiquetas se comprobó.
No se sobrescribió el PNG global original. Las interpretaciones se expresan como contribuciones
predictivas en log-odds, no causalidad. La visualización ampliada está incorporada en el notebook;
su exportación a un directorio separado ocurre al ejecutar su celda.

## 9. Cambios de código y organización

- Celda original 2: Renumeración de encabezados Markdown.
- Celda original 11: Renumeración de encabezados Markdown.
- Celda original 12: Reutilización validada; creación exclusiva solo cuando falta el CSV.
- Celda original 13: Renumeración de encabezados Markdown.
- Celda original 17: Renumeración de encabezados Markdown.
- Celda original 19: Renumeración de encabezados Markdown.
- Celda original 21: Renumeración de encabezados Markdown.
- Celda original 23: Renumeración de encabezados Markdown.
- Celda original 26: Renumeración de encabezados Markdown.
- Celda original 28: Renumeración de encabezados Markdown.
- Celda original 29: Validación del maestro preliminar persistido.
- Celda original 30: Renumeración de encabezados Markdown.
- Celda original 33: Renumeración de encabezados Markdown.
- Celda original 37: Renumeración de encabezados Markdown.
- Celda original 39: Renumeración de encabezados Markdown.
- Celda original 43: Renumeración de encabezados Markdown.
- Celda original 45: Renumeración de encabezados Markdown.
- Celda original 46: Validación de datasets integrados existentes.
- Celda original 47: Renumeración de encabezados Markdown.
- Celda original 49: Renumeración de encabezados Markdown.
- Celda original 51: Renumeración de encabezados Markdown.
- Celda original 53: Renumeración de encabezados Markdown.
- Celda original 55: Renumeración de encabezados Markdown.
- Celda original 57: Renumeración de encabezados Markdown.
- Celda original 60: Renumeración de encabezados Markdown.
- Celda original 64: Renumeración de encabezados Markdown.
- Celda original 66: Renumeración de encabezados Markdown.
- Celda original 68: Renumeración de encabezados Markdown.
- Celda original 70: Renumeración de encabezados Markdown.
- Celda original 72: Renumeración de encabezados Markdown.
- Celda original 73: Rutas de salida aisladas; parámetros y cálculos experimentales conservados.
- Celda original 74: Renumeración de encabezados Markdown.
- Celda original 77: Renumeración de encabezados Markdown.
- Celda original 78: Rutas de salida aisladas; parámetros y cálculos experimentales conservados.
- Celda original 80: Renumeración de encabezados Markdown.
- Celda original 82: Renumeración de encabezados Markdown.
- Celda original 83: Rutas de salida aisladas; parámetros y cálculos experimentales conservados.
- Celda original 85: Renumeración de encabezados Markdown.
- Celda original 87: Renumeración de encabezados Markdown.
- Celda original 89: Renumeración de encabezados Markdown.
- Celda original 91: Renumeración de encabezados Markdown.
- Celda original 92: Rutas de salida aisladas; parámetros y cálculos experimentales conservados.
- Celda original 93: Renumeración de encabezados Markdown.
- Celda original 94: Rutas de salida aisladas; parámetros y cálculos experimentales conservados.
- Celda original 95: Renumeración de encabezados Markdown.

Además se añadieron la validación reutilizable, el bloque original recuperado, los tres
complementos metodológicos, interpretaciones y la visualización SHAP ampliada. Las celdas
de experimentos, evaluación final, contribuciones SHAP y selección de casos conservan su
contenido matemático; las modificaciones de rutas en bloques de exportación evitan
sobrescribir evidencias. No se fusionaron celdas ni se eliminaron auditorías o celdas vacías.

La numeración de comentarios de código de bloques originales se conserva como trazabilidad;
la numeración académica de secciones se presenta en Markdown. El mapeo de posiciones sigue:

| Celda original | Celda final | Tipo | Ejecución guardada |
| --- | --- | --- | --- |
| 1 | 1 | code | None |
| 2 | 2 | markdown |  |
| 3 | 4 | code | 1 |
| 4 | 5 | markdown |  |
| 5 | 6 | markdown |  |
| 6 | 7 | code | 2 |
| 7 | 8 | markdown |  |
| 8 | 9 | code | 3 |
| 9 | 10 | markdown |  |
| 10 | 11 | code | 4 |
| 11 | 12 | markdown |  |
| 12 | 14 | code | 5 |
| 13 | 16 | markdown |  |
| 14 | 17 | code | 6 |
| 15 | 18 | code | 7 |
| 16 | 19 | code | 8 |
| 17 | 20 | markdown |  |
| 18 | 21 | code | 9 |
| 19 | 22 | markdown |  |
| 20 | 23 | code | 10 |
| 21 | 24 | markdown |  |
| 22 | 25 | code | 12 |
| 23 | 26 | markdown |  |
| 24 | 27 | code | 13 |
| 25 | 28 | code | 14 |
| 26 | 29 | markdown |  |
| 27 | 30 | code | 15 |
| 28 | 31 | markdown |  |
| 29 | 32 | code | 16 |
| 30 | 33 | markdown |  |
| 31 | 34 | code | 17 |
| 32 | 35 | code | 18 |
| 33 | 36 | markdown |  |
| 34 | 37 | code | 20 |
| 35 | 38 | code | 22 |
| 36 | 40 | code | 23 |
| 37 | 41 | markdown |  |
| 38 | 42 | code | 24 |
| 39 | 43 | markdown |  |
| 40 | 44 | code | 25 |
| 41 | 45 | markdown |  |
| 42 | 46 | code | 26 |
| 43 | 64 | markdown |  |
| 44 | 65 | code | 27 |
| 45 | 47 | markdown |  |
| 46 | 48 | code | 28 |
| 47 | 49 | markdown |  |
| 48 | 50 | code | 29 |
| 49 | 51 | markdown |  |
| 50 | 52 | code | 30 |
| 51 | 66 | markdown |  |
| 52 | 67 | code | 31 |
| 53 | 68 | markdown |  |
| 54 | 69 | code | 32 |
| 55 | 70 | markdown |  |
| 56 | 71 | code | 33 |
| 57 | 72 | markdown |  |
| 58 | 73 | code | 34 |
| 59 | 74 | code | 36 |
| 60 | 75 | markdown |  |
| 61 | 76 | code | 38 |
| 62 | 77 | code | 40 |
| 63 | 79 | code | 41 |
| 64 | 80 | markdown |  |
| 65 | 82 | code | 44 |
| 66 | 83 | markdown |  |
| 67 | 84 | code | 45 |
| 68 | 85 | markdown |  |
| 69 | 86 | code | 46 |
| 70 | 87 | markdown |  |
| 71 | 88 | code | 47 |
| 72 | 89 | markdown |  |
| 73 | 90 | code | 49 |
| 74 | 91 | markdown |  |
| 75 | 92 | code | 50 |
| 76 | 93 | code | 51 |
| 77 | 95 | markdown |  |
| 78 | 96 | code | 52 |
| 79 | 97 | code | 53 |
| 80 | 98 | markdown |  |
| 81 | 99 | code | 54 |
| 82 | 100 | markdown |  |
| 83 | 101 | code | 55 |
| 84 | 103 | code | 57 |
| 85 | 104 | markdown |  |
| 86 | 105 | code | 59 |
| 87 | 106 | markdown |  |
| 88 | 107 | code | 60 |
| 89 | 110 | markdown |  |
| 90 | 111 | code | 61 |
| 91 | 113 | markdown |  |
| 92 | 114 | code | 63 |
| 93 | 53 | markdown |  |
| 94 | 54 | code | 64 |
| 95 | 55 | markdown |  |
| 96 | 56 | code | 66 |
| 97 | 116 | code | None |

## 10. Comprobaciones y límites

- Validación nbformat 4.5: aprobada en lectura y escritura del archivo final.
- Conservación de las 97 celdas originales, identificadores y 251 salidas: igualdad exacta.
- Conservación de explicaciones originales fuera de encabezados: comprobada.
- Análisis estático de referencias de módulo, importaciones y orden de definiciones: sin
  referencias no resueltas detectadas tras recuperar la preparación.
- La comprobación estática no prueba todos los caminos condicionales, dependencias del
  entorno, tiempos de ejecución ni identidad de etiquetas de clustering.
- Entorno de verificación: Python del proyecto con pandas 3.0.5, numpy 2.5.2;
  no se instalaron ni actualizaron bibliotecas.
- Entrenamientos supervisados ejecutados: 0. Entrenamientos K-Means/GMM ejecutados: 0.
- Se probaron lecturas, uniones complementarias, particiones, escalado/PCA de preparación,
  transformaciones del Pipeline guardado, predicciones y explicaciones de integridad.
- El archivo sigue usando rutas Windows del proyecto; no se certifica ejecución directa en Colab.
- No se afirma Run All completo ni cumplimiento total de la rúbrica.

## 11. Impacto de cambios futuros

Las correcciones realizadas no exigen cambiar el modelo original. El complemento de área y
la descripción ponderada no modifican el experimento. Si se decide incorporarlos como
predictores o como pesos de ajuste, o cambiar la edad/etiqueta o la semántica de categorías,
o restringir el entrenamiento a residentes habituales, sería necesario revisar y repetir
las validaciones de las configuraciones afectadas. Eso
no se realizó ni queda presentado como aprobado. Un cambio posterior requiere preservar
las métricas históricas y no reutilizar prueba para seleccionar la nueva configuración.

## 12. Fuentes verificadas

- Guía local de evaluación, páginas PDF 5–7.
- Diccionario panel 2021–2025, páginas PDF 588–590, 654, 657–658 y 660–662.
- Cuestionarios ENAHO01 y ENAHO01A de 2025; ficha técnica panel 2021–2025.
- [MINEDU–ESCALE: alumnos con atraso escolar](https://escale.minedu.gob.pe/tendencias-2016-portlet/servlet/tendencias/archivo?idCuadro=14&tipo=meta).
- [INEI: metodología de población residente y FACPOB07](https://www.inei.gob.pe/media/MenuRecursivo/publicaciones_digitales/Est/Lib1244/Libro.pdf).
- Historial local Jupyter, sesión 66, ejecución 43; consultas de lectura dirigidas a la preparación de clustering.
- CSV, figuras y joblib originales de resultados.


## 13. Verificación final de tablas y presentación

Se cotejaron automáticamente las tablas HTML guardadas del notebook original con
`01_comparacion_clasificacion.csv`, `02_comparacion_clustering.csv`,
`03_perfiles_clustering.csv` y `04_metricas_prueba.csv`: nombres, filas y valores numéricos
coinciden dentro del redondeo mostrado. Esta prueba no ajustó modelos.
La figura SHAP ampliada se inspeccionó visualmente y muestra diez características
individuales y la suma de las otras 25. Las 97 celdas originales y sus 251 salidas
continúan iguales después de la validación y de ajustar la numeración de encabezados.


La comprobación de conservación cubrió los 117 archivos presentes tras crear el respaldo
adicional: no hubo cambios ni eliminaciones. Para los notebooks, datasets procesados,
DBF y resultados se compararon también hashes; para las fuentes ENAHO originales y ZIP
se comprobaron tamaños y fechas de modificación sin volver a recorrer su contenido completo.
Las únicas incorporaciones posteriores al respaldo fueron el notebook final y este informe.
El entorno comprobado incluye scikit-learn 1.9.0, XGBoost 3.4.1, SHAP 0.54.1,
nbformat 5.11.1 y dbfread 2.0.7. No se instalaron paquetes.
