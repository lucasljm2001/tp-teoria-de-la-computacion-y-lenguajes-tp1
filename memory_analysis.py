#!/usr/bin/env python3
"""
Mide el uso de memoria (picos) de las funciones en `taylor.py` usando tracemalloc
y genera un gráfico comparativo `memory_comparison.png`.

Uso: python3 memory_analysis.py
"""

import subprocess
import sys
import os
import statistics

ROOT = os.path.dirname(os.path.abspath(__file__))

FUNCTIONS = [
    ("Horner", "taylor_e_x_horner"),
    ("Naive", "taylor_e_x_naive"),
    ("Optmizada", "taylor_e_x_optmizada"),
]

X = 4
N = 10
REPEATS = 3


def measure_peak_subprocess(func_name: str, x=X, n=N, repeats=REPEATS):
    peaks = []
    for _ in range(repeats):
        code = (
            "import tracemalloc\n"
            "import taylor\n"
            "tracemalloc.start()\n"
            f"taylor.{func_name}({x},{n})\n"
            "print(tracemalloc.get_traced_memory()[1])\n"
        )
        completed = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True)
        if completed.returncode != 0:
            raise RuntimeError(f"Error al medir {func_name}: {completed.stderr}")
        out = completed.stdout.strip()
        if not out:
            raise RuntimeError(f"Salida vacía al medir {func_name}")
        try:
            peak = int(out.splitlines()[-1])
        except Exception as e:
            raise RuntimeError(f"No pude parsear la salida: {out}") from e
        peaks.append(peak)
    return min(peaks), peaks


def main():
    results = {}
    print(f"Midiendo picos de memoria (x={X}, n={N}, repeats={REPEATS})")
    for label, func in FUNCTIONS:
        try:
            best, all_peaks = measure_peak_subprocess(func)
            results[label] = {"best": best, "all": all_peaks}
            print(f"{label}: best={best} bytes; peaks={all_peaks}")
        except Exception as e:
            print(f"Fallo medición {label}: {e}")
            sys.exit(1)

    names = list(results.keys())
    peaks_bytes = [results[n]["best"] for n in names]
    peaks_kib = [b / 1024.0 for b in peaks_bytes]

    # Intentar graficar
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        print("matplotlib no está disponible. Instale matplotlib y ejecute de nuevo.")
        print("Resumen:")
        for n in names:
            b = results[n]["best"]
            print(f"{n}: {b} bytes ({b/1024.0:.2f} KiB)")
        sys.exit(0)

    plt.figure(figsize=(6, 4))
    bars = plt.bar(names, peaks_kib, color=["#4C72B0", "#DD8452", "#55A868"]) 
    plt.ylabel("Peak memory (KiB)")
    plt.title(f"Comparativa memoria (x={X}, n={N})")
    plt.grid(axis="y", linestyle="--", alpha=0.2)
    for bar, val in zip(bars, peaks_kib):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{val:.1f} KiB", ha="center", va="bottom", fontsize=8)
    out_path = os.path.join(ROOT, "memory_comparison.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    print(f"Gráfico guardado en: {out_path}")
    print("Resumen (bytes):")
    for n in names:
        b = results[n]["best"]
        print(f"{n},{b},{b/1024.0:.2f}")


if __name__ == "__main__":
    main()
