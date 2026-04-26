# Requerimiento
Se requiere el análisis de implementaciones algoritmicas de la Serie de Taylor.

Consideraciones generales:

La serie de Taylor permite aproximar funciones trascendentes (como ex, sin(x) o cos(x)) mediante la suma de términos de un polinomio.

Objetivos

1) Análisis preliminar, considerando la expresión matemática que determina la serie y sus posibles implementaciones. Responda justificando, si considera a priori que es posible mejorar la carga computacional / complejidad algorítmica aplicando el método divide y vencerás.

2) Diseñar, implementar y realizar un análisis de complejidad temporal y espacial de dos versiones del algoritmo para calcular la aproximación de la función exponencial $e<sup>x</sup>

3) Incluir un análisis teórico de complejidad según revisiones y modelos previos disponibles.

4) Realizar un análisis empírico:

 - **Pruebas de Estrés:** Realizar mediciones de tiempo de ejecución para valores de N que varíen desde 10<sup>1</sup> hasta 10<sup>6</sup> términos.

 - **Gráficas de Rendimiento:** Generar una comparativa visual de Tiempo  vs  N.

 - **Análisis de Error:** Comparar la precisión obtenida frente a la función nativa del lenguaje 

5) Entregable

 - **Código Fuente:** Documentado.

 - **Informe de Complejidad:** Un documento que explique por qué una versión es superior a la otra basándose en el conteo de instrucciones.

 - **Conclusiones:** considerando precisión numérica y eficiencia algorítmica de los resultados obtenidos.

Requisitos y ejecución
---------------------

**Requisitos:**
- Python 3.8+ (recomendado).
- Instalar dependencias listadas en `requirements.txt`.

Instalación rápida:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Archivos principales
- `taylor.py`: contiene las implementaciones de la aproximación de e^x: `taylor_e_x_horner` (Horner), `taylor_e_x_naive` (sumatoria) y `taylor_e_x_optmizada` (iterativa optimizada).
- `benchmark_analysis.py`: script para ejecutar mediciones de tiempo, calcular errores relativos y generar una gráfica comparativa y un CSV con resultados.
- `benchmark_results.csv`: archivo de salida con los resultados del benchmark (se crea al ejecutar `benchmark_analysis.py`).
- `memory_analysis.py`: script para medir el pico de uso de memoria de las distintas implementaciones y generar la gráfica `memory_comparison.png`.

Cómo ejecutar

- Ejecutar el script de ejemplo de las implementaciones:

```bash
python taylor.py
```

- Ejecutar el benchmark (genera `benchmark_results.csv` y `performance_vs_n.png`):

```bash
python benchmark_analysis.py
```

- Ejecutar el análisis de memoria (genera `memory_comparison.png` y muestra picos en consola):

```bash
python memory_analysis.py
```

Notas
- El benchmark ejecuta cada llamada en un subproceso con un timeout por llamada definido en `benchmark_analysis.py` (variable `MAX_SECONDS_PER_CALL`).
- La gráfica compara tiempo de ejecución vs número de términos `N` usando escala log-log.

Sobre los PNG generados
----------------------

- `performance_vs_n.png`: gráfica final que se genera al terminar el benchmark. Muestra, en escala log-log, el tiempo de ejecución frente al número de términos `N` para cada implementación (`horner`, `naive` y `optmizada`). Es el artefacto principal para interpretar el rendimiento empírico y comparar la complejidad práctica entre implementaciones.
- `performance_vs_n_preliminar.png`: gráfica preliminar que se guarda si la ejecución supera el umbral definido por `PRELIM_AFTER_SECONDS`. Útil para revisiones parciales cuando el benchmark tarda y para detectar problemas tempranos (por ejemplo, una implementación que escala mal para valores pequeños de `N`).

- `memory_comparison.png`: gráfico de barras con el pico de memoria observado (en KiB) para cada implementación de `taylor.py`. Interpretación: barras más bajas indican menor uso máximo de memoria; diferencias pequeñas (<1 KiB) pueden deberse a ruido del intérprete, por lo que conviene repetir la medición o aumentar `n` para obtener diferencias significativas.
