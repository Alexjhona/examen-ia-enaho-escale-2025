# Perfiles socioeducativos y rezago escolar con ENAHO y ESCALE 2025

Proyecto de integración de datos, clustering, clasificación y explicabilidad SHAP. La entrega contiene el artículo científico final de **seis páginas**, el notebook con **118 celdas ejecutadas**, los datos y el código de reproducción. No requiere descargar microdatos de varios gigabytes para repetir el experimento distribuido.

## Archivos de entrada para la evaluación

- `Articulo_Cientifico_IA.pdf`: artículo final en plantilla IEEE A4, sin datos de autoría, con nueve figuras y ocho tablas.
- `Articulo_Cientifico_IA.docx`: versión editable del mismo artículo.
- `notebooks/AnalisisExamen_Final.ipynb`: notebook académico completo con resultados incluidos.
- `data/processed/dataset_enaho_escale_2025.csv`: cohorte principal, 19 490 filas y 58 columnas.
- `data/processed/dataset_enaho_escale_2025_area.csv`: extensión complementaria por distrito y área, conservando los predictores históricos y las 377 faltas de enlace.
- `Diccionario_Variables.csv`: 78 variables del dataset principal y sus complementos, con procedencia, escala, fórmulas, ausentes y usos.
- `auditoria/Informe_Final_Entrega.md`: evidencias y límites frente a la rúbrica.

## Estructura

```text
Entrega_Final_IA/
  Articulo_Cientifico_IA.docx
  Articulo_Cientifico_IA.pdf
  README.md
  Diccionario_Variables.csv
  requirements.txt
  requirements_documentos.txt
  notebooks/               notebook ejecutado
  src/                     ejecución, complementos, figuras e informe
  data/raw/                ZIP ESCALE y cachés ENAHO de llaves, grado y factores
  data/processed/          cuatro módulos reducidos, maestros y cohortes
  resultados/tablas/       resultados originales de referencia
  resultados/figuras/      figuras originales y composición del artículo
  resultados/modelos/     pipeline XGBoost original
  resultados/reproducido/ salidas de la ejecución desde kernel limpio
  resultados/complementarios/ ponderación, área y sensibilidad
  auditoria/               registros de ejecución, controles y manifiesto
  fuentes_y_referencias/   guía, fichas, diccionario, bibliografía y plantilla
```

`data/interim/` es una caché de DBF que el notebook crea desde los ZIP incluidos. Se excluye del ZIP y de Git para evitar duplicar las bases comprimidas. El notebook no depende de rutas personales del equipo de origen.

## Instalación y ejecución local

Entorno verificado: Windows, **Python 3.14.2 de 64 bits**. Las versiones exactas de las bibliotecas están en `requirements.txt` y `auditoria/versiones_entorno.json`. Se recomienda un entorno virtual independiente. Desde esta carpeta:

```bash
python -m venv .venv
```

Activar en PowerShell con `.venv\Scripts\Activate.ps1`, o en Linux con `source .venv/bin/activate`, y ejecutar:

```bash
python -m pip install -r requirements.txt
python -m jupyterlab
```

Abrir `notebooks/AnalisisExamen_Final.ipynb`, reiniciar el kernel y ejecutar todas las celdas en orden. La primera celda localiza la raíz desde el directorio actual o sus padres. Si el entorno abre el notebook fuera de esa estructura, establecer la variable `IA_PROJECT_ROOT` con la carpeta de entrega.

También puede ejecutarse sin interfaz:

```bash
python src/ejecutar_notebook.py
```

Este comando crea un kernel limpio con el mismo Python que lo invoca, descarta las salidas previas en memoria y guarda una nueva copia en `resultados/reproducido/AnalisisExamen_Ejecutado.ipynb`; conserva el notebook entregado. Registra el estado en `resultados/reproducido/registro_ejecucion.json`. El tiempo depende del equipo; la primera reproducción verificada tardó 103,18 segundos. No se usa GPU.

## Uso en Colab

Extraer la carpeta completa en el entorno o montarla desde Drive. No basta con cargar el `.ipynb` aislado. Instalar las dependencias, cambiar el directorio a la carpeta de entrega y ejecutar el notebook completo. Si la versión de Python de Colab no admite las versiones fijadas, utilizar un entorno compatible y documentar los cambios; la prueba certificada se realizó en el entorno local indicado, no en Colab.

## Protocolo experimental

Semilla 42. GroupShuffleSplit por `CONGLOME_25`: 15 610 personas de entrenamiento y 3 880 de prueba. GroupKFold de tres folds sobre entrenamiento. Las intersecciones de conglomerados son vacías. Imputación, escalado y One-Hot se ajustan dentro de cada fold; sobremuestreo y pesos de clase usan exclusivamente entrenamiento. El clasificador excluye edad, grado, edad normativa, desfase, identificadores e indicadores de cruce.

Se conservan las diez configuraciones: regresión logística y Random Forest normal/balanceada/sobremuestreada, XGBoost y LightGBM normal/balanceado. Se reproducen K-Means y GMM para k=2 a 6, el refinamiento sin códigos de pase, la evaluación final y SHAP. El ganador histórico es XGBoost balanceado, seleccionado por F1 positivo de validación, con umbral 0,5. Las cinco tablas principales de la nueva ejecución coinciden numéricamente con las referencias guardadas.

Resultados finales: ROC-AUC 0,625042; AP 0,092119; PR-AUC trapezoidal 0,089826; F1 positivo 0,112652; F1 macro 0,478821. Matriz de confusión `[[2791, 938], [86, 65]]`. La precisión positiva 0,064806 y la calibración insuficiente limitan la utilidad predictiva.

## Complementos y fuentes del artículo

```bash
python src/exportar_complementos.py
python src/ajuste_complementario.py
python src/figuras_articulo.py
```

El primer comando exporta FACPOB07, cobertura por área y la tabla contextual sin cambiar el modelo. El segundo ejecuta 4 combinaciones XGBoost × 3 folds únicamente en entrenamiento: profundidades 3/4 y 100/150 árboles. Es una sensibilidad posterior acotada; no reemplaza la selección histórica ni evalúa nuevas configuraciones en prueba. El tercero regenera las figuras compactas a partir de los mismos datos y modelo. Los originales de referencia permanecen en sus carpetas separadas.

Para regenerar Word instalar `requirements_documentos.txt` y ejecutar `python src/crear_articulo.py`. La plantilla IEEE auténtica utilizada y su procedencia están en `fuentes_y_referencias/`. La exportación PDF reproducida usa Microsoft Word en Windows: `powershell -File src/exportar_pdf_word.ps1`. Cambiar de motor puede alterar la paginación; el PDF incluido ya está revisado y tiene seis páginas.

## Procedencia y alcance de los datos

La guía del examen remite al repositorio compartido ENAHO–ESCALE. Se usaron los archivos panel 2021–2025 proporcionados, seleccionando el corte `_25`; no se certifica equivalencia total con la base anual independiente. Se conservan los cuatro extractos reducidos originales y dos cachés adicionales (factores/residencia y grado/tipo de centro). Se incluyen los ZIP válidos de Padrón y Padlocal. Las fuentes gigantes, módulos ajenos al experimento, ZIP inválidos y múltiples respaldos del notebook se conservan fuera de esta entrega.

`src/extraer_corte_panel.py` permite volver a extraer las columnas del corte 2025 desde los cuatro CSV panel completos, hacia una carpeta nueva. Esa ruta completa de lectura de varios gigabytes no forma parte de la reproducción certificada: esta usa los extractos incluidos. No confundir lectura reproducible de los extractos con reconstrucción íntegra desde cada archivo fuente original.

Limitaciones científicas: edad a entrevista en lugar del 31 de marzo; modalidades EBR/CEBA no totalmente aisladas; códigos de pase conservados; indicadores históricos solo distritales; contexto por área con 377 ausentes; ingreso/gasto totales y no per cápita; ausencia de conectividad escolar, frecuencia TIC y altitud en el modelo; métricas sin pesos del diseño muestral. FACPOB07 se usa solo en descripción de residentes de entrenamiento y FACTOR07 se conserva como referencia de hogar. No se atribuye causalidad, representatividad nacional ni utilidad para decisiones automáticas sobre estudiantes.

## Integridad y repositorio

```bash
python src/verificar_integridad.py
```

El manifiesto contiene tamaño y SHA-256 de los archivos finales (excepto el propio manifiesto). Los registros de auditoría históricos describen estados anteriores; `Informe_Final_Entrega.md` y `ejecucion_kernel_limpio.json` documentan la entrega actual. Los originales y respaldos del proyecto principal se conservaron.

Este repositorio conserva la estructura de la entrega final. El PDF del artículo, el notebook y los datos procesados están disponibles directamente en sus rutas. La entrega se publica en GitHub por solicitud expresa del estudiante. Los DBF intermedios se regeneran y están excluidos mediante `.gitignore`. La defensa oral corresponde al estudiante; el informe documenta evidencias y no asigna una nota oficial.

## Acceso a los productos

- [Artículo final PDF](Articulo_Cientifico_IA.pdf)
- [Artículo editable Word](Articulo_Cientifico_IA.docx)
- [Notebook ejecutado](notebooks/AnalisisExamen_Final.ipynb)
- [Dataset procesado](data/processed/dataset_enaho_escale_2025.csv)
- [Diccionario de variables](Diccionario_Variables.csv)

El ZIP de entrega contiene los mismos productos académicos. Los registros internos de auditoría reflejan la validación previa a la publicación; la copia de GitHub actualiza este README y su manifiesto sin alterar los resultados.
